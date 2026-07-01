class SectionGraph:
    """
    Deterministic ordering system for document sections.
    Replaces insertion logic with compile-time ordering guarantees.
    """

    ORDER = ["8.1", "8.2", "9"]

    def sort(self, sections):
        order_index = {k: i for i, k in enumerate(self.ORDER)}
        return sorted(sections, key=lambda s: order_index.get(s.id, 9999))
