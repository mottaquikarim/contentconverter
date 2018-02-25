class UnacceptableCritera(Exception):
    pass


class NotAcceptingLines(Exception):
    pass


class VSlide(object):
    new_slide_criteria = '#'
    title_slide_criteria = '# '
    pre_swap_criteria = [('---', '')]

    @classmethod
    def add_line_or_create(cls, line, prev_cls=None):
        try:
            return cls(line)
        except (UnacceptableCritera, NotAcceptingLines):
            if prev_cls and prev_cls.acceptingLines:
                prev_cls.add_line(line)
                return None

            return cls(line, force=True)

    @staticmethod
    def impl_pre_swaps(line):
        for crit in VSlide.pre_swap_criteria:
            line = line.replace(crit[0], crit[1])

        return line

    def __init__(self, line, force=False):
        if not line.startswith(VSlide.new_slide_criteria) and not force:
            raise UnacceptableCritera('line does not begin with acceptable criteria')

        self.acceptingLines = True
        self.contents = []
        self.add_line(line)

    def add_line(self, line):
        if not self.acceptingLines:
            raise NotAcceptingLines('vslide is no longer accepting lines')

        line = VSlide.impl_pre_swaps(line)
        if line != "":
            self.contents.append(line)

        if line.startswith(VSlide.title_slide_criteria):
            self.acceptingLines = False

    def __repr__(self):
        return "\n".join(self.contents)


class Converter(object):

    @staticmethod
    def assemble(content):
        slides = []
        for c in content:
            lines = c.splitlines()
            vslide = []
            for line in lines:
                if len(vslide) == 0:
                    vslide.append(VSlide(line))
                    continue

                vs = VSlide.add_line_or_create(line, vslide[-1])
                if vs:
                    vslide.append(vs)

            slides.append(vslide)

        return slides

    def __init__(self, content):
        self.slides = self.assemble(content)

    @property
    def exportable(self):
        str_ = ''
        for slide in self.slides:
            vstr = ''
            for vslide in slide:
                vstr = str(vslide) if vstr == '' else vstr + "\n\n-\n\n" + str(vslide)

            str_ = vstr if str_ == '' else str_ + "\n---\n" + vstr

        return str_
