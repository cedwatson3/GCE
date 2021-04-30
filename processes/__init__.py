def make_readable_name(var_name: str):
    """
    Returns a more user-friendly/readable version of var_name.

    e.g. user_id -> User id; year_group -> Year group
    """
    return ' '.join(var_name.split('_')).capitalize()


def shorten_string(s: str, max_length: int):
    """
    If longer than max_length, truncates string s and appends '...'.
    Final string length will always be <= max_length
    """
    if len(s) > max_length:
        return s[:max_length - 3] + '...'
    else:
        return s


def make_multiline_string(s: str, max_line_length: int):
    """
    Converts string s into a string with \n separators that ensure
    that each line of text is no longer than line_length characters long.
    Line breaks only occur on spaces, not within words.
    """
    if max_line_length < 15:
        raise ValueError('Please use a line_length value of at least 15')
    words = s.split(' ')
    final_string = ''
    current_line_length = 0
    for w in words:
        word_length = len(w)

        if current_line_length + word_length > max_line_length:
            final_string = final_string[:-1] + '\n'  # [:-1] removes trailing space
            current_line_length = 0

        current_line_length += word_length
        final_string += w + ' '

    return final_string[:-1]  # removes trailing space
