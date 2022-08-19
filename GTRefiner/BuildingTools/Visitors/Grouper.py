import warnings
from abc import abstractmethod
from typing import List

import numpy as np

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import Layout, TextRegion


class Grouper(Visitor):

    @abstractmethod
    def visit_page(self, page: Page):
        """ No default implementation available for the Grouper.
        """
        pass

    @abstractmethod
    def group(self, region: TextRegion) -> TextRegion:
        """ Groups all layouts  class: `Layout` within a region class: `TextRegion`.
        :param region: Region to be (re-)grouped
        :type region: TextRegion
        :return: grouped Region
        :rtype: TextRegion
        """
        pass


class BlockGrouper(Grouper):
    """ Groups the elements of the :class: `Layout` given into different blocks depending on their minimal x-coordinate.
        Takes use of the np.histogram to group into different bins.
        :param layout_class: Layout-class to be grouped.
        :type layout_class: LayoutClasses
    """

    def __init__(self, layout_class: LayoutClasses):
        """Constructor method
        """
        self.layout_class = layout_class

    def visit_page(self, page: Page):
        """Groups all the elements of the layout-class :class: `LayoutClasses` of this instance."""
        regions = page.vector_gt.regions
        for i, region in enumerate(regions):
            if self.layout_class == region.layout_class:
                regions[i] = self.group(region)

    def group(self, region: TextRegion, bins: int = 6) -> TextRegion:
        """ Detect clusters based on x value of page elements.
        :param region: region to be sorted.
        :type region: TextRegion
        :param bins: number of x-oriented bins, defaults to 6
        :type bins: int
        :return: returns the given amount of bins (or less) see numpy documentation
        :rtype: List[PageElement]
        """
        if len(region.text_regions) == 0:
            raise AttributeError("Can't sort a TextRegion without Layouts.")
        if len(region.text_regions) > 1:
            warnings.warn(
                f"The Text Region already contains {len(region.text_regions)} blocks. "
                f"They will be concatenated and regrouped.")
        # initialize page_elems
        page_elems: List[PageElement] = []
        for region in region.text_regions:
            page_elems.extend(region.page_elements)
        return self._get_horizontal_clusters(text=page_elems, layout_class=self.layout_class, bins=bins)

    def _get_horizontal_clusters(self, text: List[PageElement], layout_class: LayoutClasses,
                                 bins: int = 6) -> TextRegion:
        """ Group on X axis. """
        polygons_min_x: List[int] = [l.polygon.get_min_x() for l in text]
        histo, bin_ranges = np.histogram(a=polygons_min_x, bins=bins)
        # remove last bin to fix the problem of outlayers
        bin_indexes = np.digitize(x=polygons_min_x, bins=bin_ranges[:-1])

        blocks = {}
        for i, bin_idx in enumerate(bin_indexes):
            if bin_idx not in blocks:
                blocks[bin_idx] = []
            blocks[bin_idx].append(text[i])

        text_region = TextRegion()
        for a in [p for p in blocks.values()]:
            text_region.add_region(Layout(page_elements=a, layout_class=layout_class))

        return text_region


class ThresholdGrouper(Grouper):
    """ Threshold grouper splits regions if their elements are too far apart (only if both the x and y threshold are
    exceeded).
    :param x_threshold: x threshold in pixels to define determin if an element should be split off.
    :type x_threshold: int
    :param y_threshold: y threshold in pixels to define determin if an element should be split off.
    :type y_threshold: int
    :param layout_class: Layout-class to be grouped.
    :type layout_class: LayoutClasses
    """

    def __init__(self, x_threshold: int, y_threshold: int, layout_class: LayoutClasses):
        """Constructor method
        """
        self.layout_class = layout_class
        self.x_threshold: int = x_threshold
        self.y_threshold: int = y_threshold

    def visit_page(self, page: Page):
        """Groups all the elements of the layout-class :class: `LayoutClasses` of this instance.
        :param page: page to be grouped
        :type page: Page
        """
        regions = page.vector_gt.regions
        grouped_regions: List[TextRegion] = []
        for i, region in enumerate(regions):
            if self.layout_class == region.layout_class:
                grouped_regions.append(self.group(region))
            else:
                grouped_regions.append(region)
        page.vector_gt.regions = grouped_regions

    def group(self, region: TextRegion) -> TextRegion:
        """Splits regions if their elements are too far apart (only if both the x and y threshold are
        exceeded). Warning: Make sure regions are sorted in either ascending or descending order the way a text is read.
        :param region: region to be grouped
        :type region: TextRegion
        """
        split_region = self._split_if_smaller_than_threshold(region)
        return split_region

    def _split_if_smaller_than_threshold(self, region: TextRegion):
        """
        :param region: region to be grouped
        :type region: TextRegion
        :return: new (grouped) text region.
        :rtype: TextRegion
        """
        grouped_region: List[Layout] = []
        group: Layout = Layout(page_elements=[region.text_regions[0].page_elements[0]], layout_class=self.layout_class)
        prev_elem = region.text_regions[0].page_elements[0]
        loop_counter = 0
        page_elems: List[PageElement] = []
        for region in region.text_regions:
            page_elems.extend(region.page_elements)
        for i, elem in enumerate(page_elems[1:]):
            if len(page_elems) < 1:
                break
            if len(page_elems) == 1:
                group.add_elem(elem)
                grouped_region.append(group)
                break
            # top left corner of each pagelement
            prev_x = prev_elem.polygon.get_min_x()
            prev_y = prev_elem.polygon.get_min_y()
            cur_x = page_elems[i + 1].polygon.get_min_x()
            cur_y = page_elems[i + 1].polygon.get_min_y()
            if abs(prev_y - cur_y) > self.y_threshold or abs(prev_x - cur_x) > self.x_threshold:
                grouped_region.append(group)
                group: Layout = Layout(page_elements=[page_elems[i + 1]], layout_class=self.layout_class)
            else:
                group.add_elem(elem)
            prev_elem = elem
            loop_counter = loop_counter + 1
        # assertion
        grouped_region.append(group)
        control_counter = 0
        for layout in grouped_region:
            for elem in layout:
                control_counter = control_counter + 1
        print(control_counter)
        print(loop_counter)
        # assert control_counter == loop_counter

        return TextRegion(text_regions=grouped_region)

    def _merge_if_smaller_than_threshold(self, region: TextRegion):
        """
        To be used, if there are many layouts in a region and they should be merged, if they are close together.
        :param region:
        :return:
        """
        warnings.warn("Currently not used and not tested.")
        previous_block: Layout = region[0]
        for i, block in enumerate(region[1:]):
            # top left corner of region
            prev_x = previous_block.page_elements[-1].polygon.get_min_x()
            prev_y = previous_block.page_elements[-1].polygon.get_min_y()
            cur_x = block.page_elements[-1].polygon.get_min_x()
            cur_y = block.page_elements[-1].polygon.get_min_y()
            if abs(prev_y - cur_y) < self.y_threshold and abs(prev_x - cur_x) < self.x_threshold:
                previous_block.merge(block)
                region[i].remove(block)
            else:
                previous_block = block
        return region
