from .scriptElement import ScriptElement

from exceptions import CommentTooBigError, NotInCollectionError


class VideoScript:
    def __init__(self, max_length, min_length=0, script_elements=None):
        self.script_elements = script_elements
        self.max_length = max_length
        self.min_length = min_length

        self.cur_length = 0
        self._id_count = 0

        if self.script_elements is None:
            self.script_elements = []
        else:
            self.add_script_elements(script_elements)

    @property
    def finished(self):
        return self.cur_length >= self.min_length

    @property
    def script(self) -> str:
        return "\n".join([script_element.text for script_element in self.script_elements])

    def can_add_script_element(self, script_element):
        return self.cur_length + script_element.duration <= self.max_length

    def add_script_element(self, script_element):
        if self.cur_length + script_element.duration > self.max_length:
            raise CommentTooBigError("VideoScript() max length exceeded")

        script_element.id_ = self._id_count

        self._id_count += 1

        self.script_elements.append(script_element)

        self.cur_length += script_element.duration

    def add_script_elements(self, script_elements):
        for script_element in script_elements:
            self.add_script_element(script_element)

    def get_script_element(self, id_) -> ScriptElement:
        for script_element in self.script_elements:
            if script_element.id == id_:
                return script_element

        raise NotInCollectionError(
            f"VideoScript() script element with id {id_} not found")

    def remove_script_element(self, id_):
        element = self.get_script_element(id_)

        self.cur_length -= element.duration

        self.script_elements.remove(element)

    def __len__(self):
        return len(self.script_elements)
