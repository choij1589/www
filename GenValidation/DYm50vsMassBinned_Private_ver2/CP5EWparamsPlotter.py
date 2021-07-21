from BinnedAndIncl import BinnedAndIncl
from Parameters.binned_and_incl_params import params
from ROOT import TFile, TH1D

def plot_maker(obs, norm):
    cvs_params = params[obs]["cvs_params"]
    hist_params = params[obs]['hist_params']
    info_params = params[obs]["info_params"]

    hist_name = obs
    hist_incl = None
    hists_binned = {}
    for file_name in file_names:
        dir_name = "Unknown"

        # combine ee and mm channels
        hist_path = dir_name + "/" + hist_name
        #print(hist_path + selector_arg + "_ee")
        hist_ee = root_files[file_name].Get(
            hist_path + selector_arg + "_ee")
        hist_mm = root_files[file_name].Get(
            hist_path + selector_arg + "_mm")
        hist = hist_ee.Clone(file_name + selector_arg + "_clone")
        hist.Add(hist_mm)

        xsec = xsecs[file_name]
        scale = 1.
        eff = 1.
        try:
            if norm == "genWeights":
                genWeights = root_files[file_name].Get(dir_name + "/genWeights")
                npos = genWeights.GetBinContent(genWeights.FindBin(1))
                nneg = genWeights.GetBinContent(genWeights.FindBin(-1))
                scale = xsec/(npos-nneg)
            elif norm == "Integral":
                scale = xsec/hist.Integral()
                if "j1" in obs:
                    h_nJets_ee = root_files[file_name].Get(dir_name + "/nJets_ee")
                    h_nJets_mm = root_files[file_name].Get(dir_name + "/nJets_mm")
                    h_nJets = h_nJets_ee.Clone("nJets")
                    h_nJets.Add(h_nJets_mm)
                    eff = 1. - (h_nJets.GetBinContent(h_nJets.FindBin(0.))/h_nJets.Integral())
                    print("1j binned eff:", eff)
                if "j2" in obs:
                    h_nJets_ee = root_files[file_name].Get(dir_name + "/nJets_ee")
                    h_nJets_mm = root_files[file_name].Get(dir_name + "/nJets_mm")
                    h_nJets = h_nJets_ee.Clone("nJets")
                    h_nJets.Add(h_nJets_mm)
                    eff = 1. - ((h_nJets.GetBinContent(h_nJets.FindBin(0.))+h_nJets.GetBinContent(h_nJets.FindBin(1.)))/h_nJets.Integral())
                    print("2j binned eff:", eff)
        except Exception as e:
            print("Exception occurred!", obs, e)
            continue

        hist.Scale(scale*eff*lumi*1000)

        key = file_name
        if selector_arg == "":
            file_name += "_dressedLep"
        elif selector_arg == "_prefsr":
            file_name += "_matchedGenJet"
        else:
            file_name += selector_arg

        if "012j" in file_name:
            hist_incl = hist
        else:
            hists_binned[key] = hist

    plotter = BinnedAndIncl(cvs_params, hist_params, info_params)
    plotter.get_hists(hist_incl, hists_binned)
    plotter.combine()
    if selector_arg == "":
        path = output_path + store_name + "_" + obs + "_dressedLep" + ".png"
    elif selector_arg == "_prefsr":
        path = output_path + store_name + "_" + obs + "_matchedGenJet" + ".png"
    else:
        path = output_path + store_name + "_" + obs + selector_arg + ".png"
    plotter.save(path)

# initial settings
file_names = ["DYm50_MG265_012j_nlo_ewparams_cp5", "DYm50_MG265_0j_nlo_ewparams_cp5",
            	"DYm50_MG265_1j_nlo_ewparams_cp5", "DYm50_MG265_2j_nlo_ewparams_cp5"]

xsecs = {
	"DYm50_MG265_012j_nlo_ewparams_cp5": 6383.,
	"DYm50_MG265_0j_nlo_ewparams_cp5": 5156.,
	"DYm50_MG265_1j_nlo_ewparams_cp5": 913.0,
	"DYm50_MG265_2j_nlo_ewparams_cp5": 348.6
}

observables = ["ZMass", "yZ", "ptZ", "phiZ",
                "ptl1", "ptl2", "etal1", "etal2", "phil1", "phil2", "nLeptons",
                "ptj1", "ptj2", "etaj1", "etaj2", "phij1", "phij2", "nJets"]
zboson = ['ZMass', 'yZ', 'ptZ', 'phiZ']
leptons = ['ptl1', 'ptl2', 'etal1', 'etal2', 'phil1', 'phil2', 'nLeptons']
jets = ['ptj1', 'ptj2', 'etaj1', 'etaj2', 'phij1', 'phij2', 'nJets']
deltaR = ['dRl1l2', 'dRj1l1', 'dRj1l2', 'dRj2l1', 'dRj2l2', 'dRj1j2']
lumi = 150.  # fb^-1
selector_arg = ""
output_path = "/root/workspace/GenValidation/www/VGenStudies/DYm50_MG265_nlo_ewparams_cp5_scaledWithIntegral/"
# get histograms
root_files = {}
selector_output = "/root/workspace/GenValidation/SelectorOutput/DrellYan/"
store_name = "DYm50_nlo_ewparams_cp5"
for name in file_names:
    this_path = selector_output + name + ".root"
    root_files[name] = TFile(this_path)

for obs in deltaR:
    plot_maker(obs, norm="Integral")
