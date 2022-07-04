from abc import abstractmethod

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.PageLayout import MainText, CommentText, Decorations


class LayoutVisitor:
    @abstractmethod
    def visitMainText(self, main_text: MainText):
        pass

    @abstractmethod
    def visitCommentText(self, comment_text: CommentText):
        pass

    @abstractmethod
    def visitDecorations(self, decorations: Decorations):
        pass