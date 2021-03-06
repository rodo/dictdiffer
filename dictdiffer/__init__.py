#coding=utf-8
"""
A dictionary difference calculator
Originally posted as:
http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary/1165552#1165552
"""


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = [
            set(d.keys()) for d in (current_dict, past_dict)
        ]
        self.intersect = self.current_keys.intersection(self.past_keys)

    def changes(self):
        chadd = self.added()
        chrem = self.removed()
        chmod = self.changed()
        return {'added': len(chadd),
                'removed': len(chrem),
                'changed': len(chmod)}

    def nb_changes(self):
        chadd = self.added()
        chrem = self.removed()
        chmod = self.changed()
        return len(chadd) + len(chrem) + len(chmod)

    def has_changes(self):
        return self.current_dict != self.past_dict

    def added(self):
        return self.current_keys - self.intersect

    def removed(self):
        return self.past_keys - self.intersect

    def changed(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect
                   if self.past_dict[o] == self.current_dict[o])

    def fulldiff(self):
        """Return a full diff between two dict

        - Return : dict
        """
        added = []
        changed = []
        removed = []
        for key in self.added():
            added.append({key: self.current_dict[key]})

        for key in self.removed():
            removed.append({key: self.past_dict[key]})

        for key in self.changed():
            changed.append({'key': key,
                            'old': self.past_dict[key],
                            'new': self.current_dict[key]})

        return {'added': added,
                'changed': changed,
                'removed': removed}
