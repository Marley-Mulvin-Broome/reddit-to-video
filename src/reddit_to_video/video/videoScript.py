"""Module for representing a video script

Classes:
    VideoScript: Represents a video script
"""

from reddit_to_video.exceptions import ScriptElementTooLongError, NotInCollectionError
from .scriptElement import ScriptElement


class VideoScript:
    """Represents a video script"""
    def __init__(self, max_length, min_length=0, script_elements=None, footer_elements=None):
        """Initialises a VideoScript object"""
        self.script_elements = script_elements
        self.footer_elements = footer_elements
        self.max_length = max_length
        self.min_length = min_length

        self.cur_length = 0
        self._id_count = 0

        if self.script_elements is None:
            self.script_elements = []
        else:
            self.add_script_elements(script_elements)

        if self.footer_elements is None:
            self.footer_elements = []
        else:
            self.add_script_elements(footer_elements, footer=True)

    @property
    def finished(self) -> bool:
        """Returns True if the VideoScript's current length is greater than the minimum length, False otherwise"""
        return self.cur_length >= self.min_length

    @property
    def script(self) -> str:
        """Returns the text of all the script elements in the VideoScript"""
        return "\n".join([script_element.text for script_element in self.all])

    @property
    def all(self) -> list[ScriptElement]:
        """Returns a list of all the script elements in the VideoScript, combining the script elements and footer elements"""
        return self.script_elements + self.footer_elements

    def can_add_script_element(self, script_element) -> bool:
        """Returns True if the script element can be added to the VideoScript based on duration, False otherwise"""
        return self.can_add_duration(script_element.duration)

    def can_add_duration(self, duration: float) -> bool:
        """Returns True if the duration can be added to the VideoScript, False otherwise"""
        return self.cur_length + duration <= self.max_length

    def add_script_element(self, script_element: ScriptElement, footer: bool=False):
        """Adds a script element to the VideoScript"""
        if not self.can_add_script_element(script_element):
            raise ScriptElementTooLongError(
                "VideoScript() max length exceeded")

        script_element.id_ = self._id_count

        self._id_count += 1

        if footer:
            self.footer_elements.append(script_element)
        else:
            self.script_elements.append(script_element)

        self.cur_length += script_element.duration

    def add_script_element_pair(self, script_element: ScriptElement, second_element: ScriptElement, footer: bool=False):
        """Adds a script element and a second element to the VideoScript, trreating them like the same element. Useful for adding two elements that need to be next to eachother or not at all."""
        if self.cur_length + script_element.duration + second_element.duration > self.max_length:
            raise ScriptElementTooLongError(
                "VideoScript() max length exceeded")

        script_element.id_ = self._id_count
        second_element.id_ = self._id_count + 1

        self._id_count += 2

        collection = self.script_elements

        if footer:
            collection = self.footer_elements

        collection.append(script_element)
        collection.append(second_element)

        self.cur_length += script_element.duration + second_element.duration

    def add_script_element_pairs(self, script_element_pairs: list[tuple[ScriptElement, ScriptElement]], footer=False, pbar=None) -> int:
        """Adds a list of script element pairs to the VideoScript"""
        minimum_duration = min([script_element_pair[0].duration +
                               script_element_pair[1].duration for script_element_pair in script_element_pairs])

        amount_added = 0

        for script_element_pair in script_element_pairs:
            try:
                self.add_script_element_pair(
                    script_element_pair[0], script_element_pair[1], footer=footer)
                amount_added += 1
            except ScriptElementTooLongError:
                if self.can_add_duration(minimum_duration):
                    continue
                else:
                    break

            if pbar is not None:
                pbar.update(1)

        return amount_added

    def add_script_elements(self, script_elements, footer=False, pbar=None) -> int:
        """Adds a list of script elements to the VideoScript"""
        minimum_duration = min(
            [script_element.duration for script_element in script_elements])

        amount_added = 0

        for script_element in script_elements:
            try:
                self.add_script_element(script_element, footer=footer)
                amount_added += 1
            except ScriptElementTooLongError:
                if self.can_add_duration(minimum_duration):
                    continue
                else:
                    break

            if pbar is not None:
                pbar.update(1)

        return amount_added

    def get_script_element(self, id_) -> ScriptElement:
        """Returns a script element with the given id, or raises an exception if it is not found"""
        for script_element in self.script_elements:
            if script_element.id == id_:
                return script_element, False

        for script_element in self.footer_elements:
            if script_element.id == id_:
                return script_element, True

        raise NotInCollectionError(
            f"VideoScript() script element with id {id_} not found")

    def remove_script_element(self, id_):
        """Removes a script element with the given id"""
        element, is_footer = self.get_script_element(id_)

        self.cur_length -= element.duration

        if is_footer:
            self.footer_elements.remove(element)
        else:
            self.script_elements.remove(element)

    def __len__(self):
        return len(self.script_elements)
