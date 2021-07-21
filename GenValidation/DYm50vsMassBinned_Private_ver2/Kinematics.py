from ROOT import TFile, TLegend, TH1, TH1D
from PlotterBase import PlotterBase


class Kinematics(PlotterBase):
    def __init__(self, cvs_params, hist_params, info_params):
        grid = cvs_params['grid']
        super().__init__(cvs_type="ratio", logy=False, grid=grid)
        self.hist_params = hist_params
        self.info_params = info_params
        self.__set_legend()

    def __set_legend(self):
        self.legend = TLegend(0.69, 0.60, 0.90, 0.90)

    def get_hists(self, hists):
        self.base_hist = None
        self.hists = {}
        self.ratio = {}

        # store histograms
        print("INFO: Storing histograms...")
        print("INFO: Histograms will be automatically normalized")
        for name, hist in hists.items():
            hist.Draw()
            scale = hist.Integral()
            self.hists[name] = self.__rebin(hist)
            self.hists[name].Scale(1./scale)

        self.__decorate_hists()
        self.__make_ratio()

    def __rebin(self, hist):
        try:
            # rebin histogram
            if 'rebin' in self.hist_params.keys():
                rebin = self.hist_params['rebin']
                hist.Rebin(rebin)
            # set x range
            if 'x_range' in self.hist_params.keys():
                x_range = self.hist_params['x_range']
                hist.GetXaxis().SetRangeUser(x_range[0], x_range[1])
            return hist
        except Exception as e:
            print("__rebin(): Exception occured! -> " + str(e))

    def __decorate_hists(self):
        print("INFO: y axis range will be set automatically")
        # get maximum y range
        max_y = -999.
        for name, hist in self.hists.items():
            max_y = max(max_y, hist.GetMaximum())
        y_title = self.hist_params['y_title']

        # decorate
        _color = 3
        for name in self.hists.keys():
            self.hists[name].SetStats(0)

            # line color
            self.hists[name].SetLineColor(_color)
            self.hists[name].SetLineWidth(1)
            _color += 1

            # x axis
            self.hists[name].GetXaxis().SetLabelSize(0)

            # y axis
            self.hists[name].GetYaxis().SetTitle(y_title)
            self.hists[name].GetYaxis().SetTitleSize(0.05)
            self.hists[name].GetYaxis().SetTitleOffset(0.8)
            self.hists[name].GetYaxis().SetLabelSize(0.03)
            self.hists[name].GetYaxis().SetRangeUser(0, max_y*1.3)

        # add to a legend
            self.legend.AddEntry(self.hists[name], name, 'lep')

    def __make_ratio(self):
        ratio_range = self.hist_params['ratio_range']
        x_title = self.hist_params['x_title']

        view = hists.values()
        it = iter(view)
        base_hist = next(it)
        for name, hist in self.hists.items():
            self.ratio[name] = self.hists[name].Clone(name+"ratio")
            self.ratio[name].Divide(base_hist)
            self.ratio[name].SetStats(0)
            self.ratio[name].SetTitle("")

            # x axis
            self.ratio[name].GetXaxis().SetTitle(x_title)
            self.ratio[name].GetXaxis().SetTitleSize(0.1)
            self.ratio[name].GetXaxis().SetTitleOffset(0.8)
            self.ratio[name].GetXaxis().SetLabelSize(0.08)

            # y axis
            self.ratio[name].GetYaxis().SetRangeUser(
                ratio_range[0], ratio_range[1])
            self.ratio[name].GetYaxis().SetTitle("x / Default")
            self.ratio[name].GetYaxis().SetTitleSize(0.08)
            self.ratio[name].GetYaxis().SetTitleOffset(0.5)
            self.ratio[name].GetYaxis().SetLabelSize(0.08)

    def combine(self):
        info = self.info_params['info']
        cms_text = self.info_params['cms_text']
        extra_text = self.info_params['extra_text']

        super().set_canvas()
        super().set_logo()
        super().set_info()
        super().pad_up().cd()
        for hist in self.hists.values():
            hist.Draw("hist&same")
        self.legend.Draw()
        super().info().DrawLatexNDC(0.725, 0.91, info)
        super().logo().DrawLatexNDC(0.15, 0.83, cms_text)
        super().extra_logo().DrawLatexNDC(0.15, 0.78, extra_text)

        super().pad_down().cd()
        for ratio in self.ratio.values():
            ratio.Draw("hist&same")

        super().cvs().cd()
        super().pad_up().Draw()
        super().pad_down().Draw()


if __name__ == "__main__":
    from Parameters.kinematics import params
    # get root files
    skflat_output = '/root/workspace/HcToWA/SignalStudy/2017/SignalStudy_TTToHcToWA_AToMuMu_'
    files_all = ['MHc70_MA15', 'MHc70_MA40', 'MHc70_MA65',
                 'MHc100_MA15', 'MHc100_MA25', 'MHc100_MA60', 'MHc100_MA95',
                 'MHc130_MA15', 'MHc130_MA45', 'MHc130_MA55', 'MHc130_MA90', 'MHc130_MA125',
                 'MHc160_MA15', 'MHc160_MA45', 'MHc160_MA75', 'MHc160_MA85', 'MHc160_MA120', 'MHc160_MA155']
    files_MHc70 = ['MHc70_MA15', 'MHc70_MA40', 'MHc70_MA65']
    files_MHc100 = ['MHc100_MA15', 'MHc100_MA25', 'MHc100_MA60', 'MHc100_MA95']
    files_MHc130 = ['MHc130_MA15', 'MHc130_MA45',
                    'MHc130_MA55', 'MHc130_MA90', 'MHc130_MA125']
    files_MHc160 = ['MHc160_MA15', 'MHc160_MA45', 'MHc160_MA75',
                    'MHc160_MA85', 'MHc160_MA120', 'MHc160_MA155']
    path = "1e2mu/muons_fake/"
    obs = "1/pt"
    cvs_params = params[obs]['cvs_params']
    hist_params = params[obs]['hist_params']
    info_params = params[obs]['info_params']

    # get histograms
    hists = {}
    for name in files_MHc160:
        this_path = skflat_output + name + ".root"
        this_file = TFile(this_path)
        this_hist = this_file.Get(path + obs)
        this_hist.SetDirectory(0)
        hists[name] = this_hist
    plotter = Kinematics(cvs_params, hist_params, info_params)
    plotter.get_hists(hists)
    plotter.combine()
    plotter.save("test.png")
