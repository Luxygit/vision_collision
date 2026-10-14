""""""


class DetectionPipeline:
    def __init__(self, min_area: int = 2000) -> None:
        self.min_area = min_area

    def categorise_boxes(self,
                         boxes: list[tuple[int, int, int, int]],
                         frame_width: int,
                         ) -> dict[str, list[tuple[int, int, int, int]]]:
        categorised: dict[str, list[tuple[int, int, int, int]]] = {
                "left": [],
                "center": [],
                "right": []
                                                                   }
        for x, y, w, h in boxes:
            if w * h < self.min_area:
                continue
            center_x = x + (w // 2)
            if 0 <= center_x < frame_width // 3:
                categorised["left"].append((x, y, w, h))
            elif frame_width // 3 <= center_x < (2 * frame_width) // 3:
                categorised["center"].append((x, y, w, h))
            else:
                categorised["right"].append((x, y, w, h))
        return categorised
