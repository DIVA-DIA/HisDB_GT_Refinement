from abc import abstractmethod
from operator import itemgetter
from typing import List

import numpy as np
import warnings

from HisDB_GT_Refinement.GTRefiner.BuildingTools.Visitor import Visitor
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Page import Page
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation import VectorGT, PageLayout
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageElements import PageElement
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import Decorations, CommentText, \
    MainText, Layout, TextRegion


class Grouper(Visitor):

    @abstractmethod
    def visit_page(self, page: Page):
        pass


class BlockGrouper(Grouper):
    """ Groups the elements of the :class: `Layout` given into different blocks depending on their minimal x-coordinate.
    Takes use of the np.histogram to group into different bins."""

    def visit_page(self, page: Page):
        pass

    # TODO: Write more generically and test it.
    def get_unsorted_layout(self, text: TextRegion) -> Layout:
        if len(text.text_regions) is 0:
            raise AttributeError("Can't sort a TextRegion without Layouts.")
        if len(text.text_regions) > 1:
            warnings.warn(
                f"The Text Region already contains {len(text.text_regions)} blocks. "
                f"They will be concatenated and regrouped.")
        # initialize page_elems
        page_elems: List[PageElement] = []
        for region in text.text_regions:
            page_elems.extend(region.page_elements)
        layout_class: LayoutClasses = None
        for elem in text.page_elements:
            if layout_class is None:
                layout_class = elem.layout_class
            elif elem.layout_class is not layout_class:
                warnings.warn(
                    f"The Layout given contains both {layout_class} and {elem.layout_class}. "
                    f"Are you sure you want to apply BlockGrouper to this Layout: {text}?")
        return LayoutClasses

    def _group(self, text: List[PageElement], layout_class: LayoutClasses) -> TextRegion:
        """ Group on X axis. """
        # lars' version min_x: [min(l.polygon, key=itemgetter(0))[0] for l in text.page_elements]
        polygons_min_x: List[int] = [l.polygon.get_min_x() for l in text]
        histo, bin_ranges = np.histogram(a=polygons_min_x)
        # remove last bin to fix the problem of outlayers
        bin_indexes = np.digitize(x=polygons_min_x, bins=bin_ranges[:-1])

        blocks = {}
        for i, bin_idx in enumerate(bin_indexes):
            if bin_idx not in blocks:
                blocks[bin_idx] = []
            blocks[bin_idx].append(text[i])

        text_region = TextRegion()
        for a in [p for p in blocks.values()]:
            text_region.add_elem(Layout())
        return

        polygons_per_category['comments'] = sorted_array


class ThresholdGrouper(Grouper):

    def visit_page(self, page: Page):
        pass

    def _group(self, y_threshold: int, x_threshold: int) -> None:
        self._sort_comment_blocks_by_x()
        blocks = self.get_comment_blocks()
        previous_block = blocks[0]
        for block in blocks[1:]:
            prev_x = previous_block.get_baselines()[-1][0]
            prev_y = previous_block.get_baselines()[-1][1]
            cur_x = block.get_baselines()[-1][0]
            cur_y = block.get_baselines()[-1][1]
            if abs(prev_y - cur_y) < y_threshold and abs(prev_x - cur_x) < x_threshold:
                previous_block.merge(block)
                self.text_comment_blocks['comment'].remove(block)
            else:
                previous_block = block
