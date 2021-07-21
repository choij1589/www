from ROOT import TCanvas, TLegend, TPad, THStack, TLatex


class PlotterBase:
    def __init__(self, cvs_type="default", logy=False, grid=False):
        # store information
        # legend should be made in child class
        self.cvs_type = cvs_type
        # self.leg_size = leg_size    # TODO: Update legend option
        self.logy = logy
        self.grid = grid

        # set info and logo
        # self.__set_canvas()
        # self.__set_info()
        # self.__set_logo()
        # self.__set_legend()

        # getter for child class
    def cvs(self):
        return self.cvs

    def pad_up(self):
        return self.pad_up

    def pad_down(self):
        return self.pad_down

    def info(self):
        return self.info

    def logo(self):
        return self.logo

    def extra_logo(self):
        return self.extra_logo

    def set_info(self):
        self.info = TLatex()
        self.info.SetTextSize(0.035)
        self.info.SetTextFont(42)

    def set_logo(self):
        self.logo = TLatex()
        self.extra_logo = TLatex()
        self.logo.SetTextSize(0.04)
        self.logo.SetTextFont(61)
        self.extra_logo.SetTextSize(0.035)
        self.extra_logo.SetTextFont(52)

    def set_canvas(self):
        try:
            if self.cvs_type == "default":
                self.cvs = TCanvas("cvs", "", 500, 500)
                if self.grid:
                    self.cvs.SetGrid()
                if self.logy:
                    self.cvs.SetLogy()
            elif self.cvs_type == "ratio":
                self.cvs = TCanvas("cvs", "", 800, 1000)
                self.pad_up = TPad("pad_up", "", 0, 0.25, 1, 1)
                self.pad_up.SetBottomMargin(0.02)
                if self.grid:
                    self.pad_up.SetGrid()
                if self.logy:
                    self.pad_up.SetLogy()

                self.pad_down = TPad("pad_down", "", 0, 0, 1, 0.25)
                self.pad_down.SetGrid(1)
                self.pad_down.SetTopMargin(0.08)
                self.pad_down.SetBottomMargin(0.3)
        except Exception as e:
            print("__set_canvas(): Exception Occured! " + str(e))
            # raise(AttributeError)
    # methods

    def draw(self):
        self.cvs.Draw()

    def save(self, path):
        self.cvs.SaveAs(path)
        self.cvs.Close()
