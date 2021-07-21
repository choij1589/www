from InclAndStitched import InclAndStitched
from Parameters.example_params import cvs_params, info_params, params
from ROOT import TFile

# initial settings
# you can also set multiple files_incl
files_incl = ["DYm50_MG265_012j_nlo_ewparams_cp5"]
files_stitched = ["DYm50_MG265_0j_nlo_ewparams_cp5",
                  "DYm50_MG265_1j_nlo_ewparams_cp5",
                  "DYm50_MG265_2j_nlo_ewparams_cp5"]

xsecs = {
    "DYm50_MG265_012j_nlo_ewparams_cp5": 6383.,
    "DYm50_MG265_0j_nlo_ewparams_cp5": 5156.,
    "DYm50_MG265_1j_nlo_ewparams_cp5": 913.0,
    "DYm50_MG265_2j_nlo_ewparams_cp5": 348.6
}

# below will be used the get the parameters for each plot, see Parameters/examples_params.py
zboson = ['ZMass', 'yZ', 'ptZ', 'phiZ']
leptons = ['ptl1', 'ptl2', 'etal1', 'etal2', 'phil1', 'phil2', 'nLeptons']
jets = ['ptj1', 'ptj2', 'etaj1', 'etaj2', 'phij1', 'phij2', 'nJets']
deltaR = ['dRl1l2', 'dRj1l1', 'dRj1l2', 'dRj2l1', 'dRj2l2', 'dRj1j2']
observables = zboson + leptons + jets + deltaR

lumi = 150.  # fb^-1
selector_arg = ""
output_path = "ExamplePlots/"

# get histograms
root_files = {}
dir_samples = "ExampleSamples/"
store_name = "DYm50_nlo_ewparams_cp5"
for name in files_incl:
    this_path = dir_samples + name + ".root"
    root_files[name] = TFile(this_path)
for name in files_stitched:
    this_path = dir_samples + name + ".root"
    root_files[name] = TFile(this_path)

# function to get histograms and plot
def plot_maker(obs, norm):
    hist_params = params[obs]['hist_params']

    hist_name = obs
    hists_incl = {}
    hists_stitched = {}
    # get inclusive samples
    # you can also set many inclusive samples for comparison between the versions
    for file_name in files_incl:
        #Let's get TFiles and corresponding histograms
        dir_name = "Unknown"

        # combine ee and mm channels for more stats
        # see TestSamples/*.root for the directory structure
        hist_path = dir_name + "/" + hist_name
        hist_ee = root_files[file_name].Get(
            hist_path + selector_arg + "_ee")
        hist_mm = root_files[file_name].Get(
            hist_path + selector_arg + "_mm")
        hist = hist_ee.Clone(file_name + selector_arg + "_clone")
        hist.Add(hist_mm)

		# weights
        # There is two ways to set a weight for each events, I recommend to use "genWeights"
        xsec = xsecs[file_name]
        scale = 1.
        eff = 1.
        if norm == "genWeights":
            genWeights = root_files[file_name].Get(dir_name + "/genWeights")
            npos = genWeights.GetBinContent(genWeights.FindBin(1))
            nneg = genWeights.GetBinContent(genWeights.FindBin(-1))
            scale = xsec/(npos-nneg)
        elif norm == "Integral":
            scale = xsec/hist.Integral()
            if "j2" in obs:
                h_nJets_ee = root_files[file_name].Get(dir_name + "/nJets_ee")
                h_nJets_mm = root_files[file_name].Get(dir_name + "/nJets_mm")
                h_nJets = h_nJets_ee.Clone("nJets")
                h_nJets.Add(h_nJets_mm)
                eff = 1. - ((h_nJets.GetBinContent(h_nJets.FindBin(0.)) + h_nJets.GetBinContent(h_nJets.FindBin(1.)))/h_nJets.Integral())
                print("2j incl eff:", eff)
            elif "j1" in obs:
                h_nJets_ee = root_files[file_name].Get(dir_name + "/nJets_ee")
                h_nJets_mm = root_files[file_name].Get(dir_name + "/nJets_mm")
                h_nJets = h_nJets_ee.Clone("nJets")
                h_nJets.Add(h_nJets_mm)
                eff = 1. - (h_nJets.GetBinContent(h_nJets.FindBin(0.))/h_nJets.Integral())
                print("1j incl eff:", eff)
            else:
                pass	
        hist.Scale(scale*eff*lumi*1000)

        key = file_name
        # ignore these lines, to correct some missetting from SelectorTools
        if selector_arg == "":
            file_name += "_dressedLep"
        elif selector_arg == "_prefsr":
            file_name += "_matchedGenJet"
        else:
            file_name += selector_arg

        hists_incl[key] = hist

    # get stitched samples
    # they will be used to make THStack
    for file_name in files_stitched:
        dir_name = "Unknown"

        # combine ee and mm channels
        hist_path = dir_name + "/" + hist_name
        hist_ee = root_files[file_name].Get(
            hist_path + selector_arg + "_ee")
        hist_mm = root_files[file_name].Get(
            hist_path + selector_arg + "_mm")
        hist = hist_ee.Clone(file_name + selector_arg + "_clone")
        hist.Add(hist_mm)

        xsec = xsecs[file_name]
        scale = 1.
        eff = 1.
        if norm == "genWeights":
            genWeights = root_files[file_name].Get(dir_name + "/genWeights")
            npos = genWeights.GetBinContent(genWeights.FindBin(1))
            nneg = genWeights.GetBinContent(genWeights.FindBin(-1))
            scale = xsec/(npos-nneg)
        elif norm == "Integral":
            scale = xsec/hist.Integral()
            if "j2" in obs:
                h_nJets_ee = root_files[file_name].Get(dir_name + "/nJets_ee")
                h_nJets_mm = root_files[file_name].Get(dir_name + "/nJets_mm")
                h_nJets = h_nJets_ee.Clone("nJets")
                h_nJets.Add(h_nJets_mm)
                eff = 1. - ((h_nJets.GetBinContent(h_nJets.FindBin(0.))+h_nJets.GetBinContent(h_nJets.FindBin(1.)))/h_nJets.Integral())
                print("2j binned eff:", eff)
            elif "j1" in obs:
                h_nJets_ee = root_files[file_name].Get(dir_name + "/nJets_ee")
                h_nJets_mm = root_files[file_name].Get(dir_name + "/nJets_mm")
                h_nJets = h_nJets_ee.Clone("nJets")
                h_nJets.Add(h_nJets_mm)
                eff = 1. - (h_nJets.GetBinContent(h_nJets.FindBin(0.))/h_nJets.Integral())
                print("1j binned eff:", eff)
            else:
                pass
        hist.Scale(scale*eff*lumi*1000)

        key = file_name
        if selector_arg == "":
            file_name += "_dressedLep"
        elif selector_arg == "_prefsr":
            file_name += "_matchedGenJet"
        else:
            file_name += selector_arg

        hists_stitched[key] = hist

    # plotter will eat inclusive and stitched samples and decorate the plots
    # note that you can change parameters defined in Parameters/example_params.py for fine settings
    plotter = InclAndStitched(cvs_params, hist_params, info_params)
    plotter.get_hists(hists_incl, hists_stitched)
    plotter.combine()
    if selector_arg == "":
        path = output_path + store_name + "_" + obs + "_dressedLep" + ".png"
    elif selector_arg == "_prefsr":
        path = output_path + store_name + "_" + obs + "_matchedGenJet" + ".png"
    else:
        path = output_path + store_name + "_" + obs + selector_arg + ".png"
    plotter.save(path)

if __name__=="__main__":
    for obs in leptons:
        try:
            plot_maker(obs, norm="genWeights")
        except Exception as e:
            print("WARNING: Exception Occurred!", e)

