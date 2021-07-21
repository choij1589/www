#import sys
#sys.path.remove('/opt/ohpc/pub/apps/root_6_12_06/lib')
from ROOT import TFile, THStack, TLegend
from PlotterBase import PlotterBase


class InclAndStitched(PlotterBase):
    """Plot several Incl samples simultaneously"""

    def __init__(self, cvs_params, hist_params, info_params):
        logy = cvs_params['logy']
        grid = cvs_params['grid']
        super().__init__(cvs_type="ratio", logy=logy, grid=grid)
        self.hist_params = hist_params
        self.info_params = info_params
        self.__set_legend()
        self.colors = [46, 9, 6, 8, 4, 12, 28]

    def __set_legend(self):
        self.legend = TLegend(0.30, 0.60, 0.90, 0.88)
        self.legend.SetNColumns(2)
        self.legend.SetFillStyle(0)
        self.legend.SetBorderSize(0)

    def get_hists(self, hs_incl, hs_stitched):
        self.hs_incl = {}
        self.hs_stitched = {}
        self.stack = THStack("stck", "")
        self.syst = None
        self.ratios = {}
        self.ratios_syst = {}

        # store histograms
        print("INFO: Stroing histograms...")
        print("INFO: histograms automatically normalized to L = 150 fb^-1")
        for name, hist in hs_incl.items():
            self.hs_incl[name] = self.__rebin(hist)
        for name, hist in hs_stitched.items():
            self.hs_stitched[name] = self.__rebin(hist)

        self.__decorate_hists()
        self.__make_stack_and_syst()
        self.__make_ratios()

    def __rebin(self, hist):
        if "rebin" in self.hist_params.keys():
            rebin = self.hist_params['rebin']
            hist.Rebin(rebin)

        # set x range
        if "x_range" in self.hist_params.keys():
            x_range = self.hist_params['x_range']
            hist.GetXaxis().SetRangeUser(x_range[0], x_range[1])

        return hist

    def __decorate_hists(self):
        print("INFO: Decorating histograms...")
        print("INFO: y axis range set to be maximum of inclusive plots")
        y_range = max([hist.GetMaximum() for hist in self.hs_incl.values()])
        y_title = self.hist_params['y_title']

        # decorate
        if len(self.hs_incl.keys()) == 1:
            print("INFO: Only one inclusive sample detected, initiate comparison between incl and stitched.")
            for name, hist in self.hs_incl.items():
                hist.SetStats(0)
                hist.SetMarkerStyle(8)
                hist.SetMarkerSize(0.5)
                hist.SetMarkerColor(1)

                # x axis
                hist.GetXaxis().SetLabelSize(0)

                # y axis
                hist.GetYaxis().SetTitle(y_title)
                hist.GetYaxis().SetRangeUser(0, y_range*1.5)
                if self.logy:
                    hist.GetYaxis().SetRangeUser(1, y_range*100000)

                # add to legend
                self.legend.AddEntry(hist, name, "lep")
        else:
            print("INFO: Several inclusive samples detected, initiate comaprision between versions.")
            color_ = 0
            for name, hist in self.hs_incl.items():
                hist.SetStats(0)
                hist.SetLineColor(self.colors[color_])
                hist.SetLineWidth(2)
                color_ += 1

                # x axis
                hist.GetXaxis().SetLabelSize(0)

                # y axis
                hist.GetYaxis().SetTitle(y_title)
                hist.GetYaxis().SetRangeUser(0, y_range*1.5)
                if self.logy:
                    hist.GetYaxis().SetRangeUser(1, y_range*1000)

                # add to legend
                self.legend.AddEntry(hist, name, 'lep')

    def __make_stack_and_syst(self):
        for name, hist in self.hs_stitched.items():
            hist.GetXaxis().SetLabelSize(0)
            self.stack.Add(hist)
            self.legend.AddEntry(hist, name, 'f')

            if self.syst == None:
                self.syst = hist.Clone("syst")
            else:
                self.syst.Add(hist)

        self.stack.Draw()   # need to draw stack first to change axis
        self.stack.GetHistogram().GetXaxis().SetLabelSize(0)
        self.syst.SetStats(0)
        self.syst.SetFillColorAlpha(12, 0.6)

        self.syst.SetFillStyle(3001)
        self.syst.GetXaxis().SetLabelSize(0)
        self.legend.AddEntry(self.syst, 'stat error', 'f')

    def __make_ratios(self):
        ratio_range = self.hist_params['ratio_range']
        x_title = self.hist_params['x_title']

        for name, hist in self.hs_incl.items():
            #hist.SetDirectory(0)
            self.ratios[name] = hist.Clone(name + "_ratio")
            self.ratios[name].Divide(self.syst)
            self.ratios_syst[name] = self.ratios[name].Clone(
                name + "_ratio_syst")

        for name, ratio in self.ratios.items():
            ratio.SetStats(0)
            ratio.SetTitle("")

            # x axis
            ratio.GetXaxis().SetTitle(x_title)
            ratio.GetXaxis().SetTitleSize(0.1)
            ratio.GetXaxis().SetTitleOffset(0.8)
            ratio.GetXaxis().SetLabelSize(0.08)

            # y axis
            ratio.GetYaxis().SetRangeUser(ratio_range[0], ratio_range[1])
            ratio.GetYaxis().SetTitle("Incl / binned")
            ratio.GetYaxis().CenterTitle()
            ratio.GetYaxis().SetTitleSize(0.08)
            ratio.GetYaxis().SetTitleOffset(0.5)
            ratio.GetYaxis().SetLabelSize(0.08)

        for name, ratio_syst in self.ratios_syst.items():
            ratio_syst.SetStats(0)
            ratio_syst.SetFillStyle(3001)
            if len(self.hs_incl.keys()) == 1:
                ratio_syst.SetFillColorAlpha(13, 0.6)

    def combine(self):
        info = self.info_params['info']
        cms_text = self.info_params['cms_text']
        extra_text = self.info_params['extra_text']

        super().set_canvas()
        super().set_logo()
        super().set_info()
        super().pad_up().cd()
        for name, hist in self.hs_incl.items():
            hist.Draw()
        self.stack.Draw("hist&pfc&same")
        self.syst.Draw("e2&f&same")
        if len(self.hs_incl.keys()) == 1:
            for name, hist in self.hs_incl.items():
                hist.Draw("p&hist&same")
                hist.Draw("e1&same")
        else:
            for name, hist in self.hs_incl.items():
                hist.Draw("pmc&hist&same")
                hist.Draw("pmc&e1&same")
        self.legend.Draw()
        super().info().DrawLatexNDC(0.72, 0.91, info)
        super().logo().DrawLatexNDC(0.15, 0.83, cms_text)
        super().extra_logo().DrawLatexNDC(0.15, 0.78, extra_text)

        super().pad_down().cd()
        if len(self.hs_incl.keys()) == 1:
            for name, ratio in self.ratios.items(): 
                ratio.Draw("p&hist&same") 
            for name, ratio_syst in self.ratios_syst.items():
                ratio_syst.Draw("e2&f&same")
            for name, ratio in self.ratios.items(): 
                ratio.Draw("p&hist&same")
        else:
            for name, ratio in self.ratios.items(): 
                ratio.Draw("pmc&hist&same")
            for name, ratio_syst in self.ratios_syst.items():
                ratio_syst.Draw("e2&f&same")
            for name, ratio in self.ratios.items(): 
                ratio.Draw("pmc&hist&same")

        super().cvs().cd()
        super().pad_up().Draw()
        super().pad_down().Draw()
