import marko

from core.lesson import Lesson, Segment


def parse(lesson_str: str) -> Lesson:
    with open(lesson_str, 'r', encoding="utf-8") as file:
        content = file.read()
    document = marko.parse(content)

    title_str = "DEFAULT"
    segments = []
    current_segment = None
    current_section = None
    result = {}

    for node in document.children:
        if isinstance(node, marko.block.Heading) and node.level == 1:
            title_str = node.children[0].children
            continue

        if isinstance(node, marko.block.Heading) and node.level == 2:
            segment_title = node.children[0].children
            current_segment = segment_title
            result[current_segment] = {}
            continue

        if current_segment and isinstance(node, marko.block.Heading) and node.level == 3:
            current_section = node.children[0].children
            result[current_segment][current_section] = ""
            continue

        if current_segment and current_section and (isinstance(node, marko.block.Paragraph)):
            result[current_segment][current_section] += node.children[0].children + "\n"
            continue

        if current_segment and current_section and (isinstance(node, marko.block.FencedCode)):
            result[current_segment][current_section] += "Code:" + node.children[0].children + "\n"

    for segment in result:
        segments.append(Segment(
            title=segment,
            theory=result.get(segment).get("theory"),
            practice=result.get(segment).get("practice"),
            answer=result.get(segment).get("answer"),
        ))
    return Lesson(title=title_str, segments=segments)

def main():
    lesson = parse(lesson_str='../data/test_lesson.md')
    print(f"{lesson.title=}")
    for segment in lesson.segments:
        print(f"{segment.title=}")
        print(f"{segment.theory=}")
        print(f"{segment.practice=}")
        print(f"{segment.answer=}")

if __name__ == '__main__':
    main()