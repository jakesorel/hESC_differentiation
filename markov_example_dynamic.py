from markov_simulator_dynamic import Markov_fit
import numpy as np
import matplotlib.pyplot as plt

transitions_possible = ("P->A","P->M","M->E","P->X")
run_params = {"initial_state":"P", ##This is the state that all of the cells are initially found in
               "dt":0.01, ##set your time discretisation
               "tfin":3.01, ##set the final time (although this dynamically changes in the simulation)
               "allow_all":False,##you can over-ride the above specification of which transitions are possible or not, saying that all transitions are possible.
               "init_mult":0.1, ##Some unnecessary parameter used in initialisation, basically preventing the rates going too high
              "states":["P","A","E","M","X"]## in the case of having 'allow_all' be True, then you need to specify what are the states
              }

##Set the plot parameters, specifying the colours of your various (measurable) variables. Can use whichever mpl colourmap you want.
plot_params = {"colour_dict":{"A":plt.cm.Oranges,
               "M":plt.cm.Reds,
               "E":plt.cm.Blues},
               "vmax":0.7 ##this caps the highest proportion plotted.
               }

opt_params = {"minimizer_params": {"maxiter": 1000},  ##dial this for increasing precision.
              "n_iter": 4 ##The number of random initialisations you would like to run. This all runs in parallel.
              }


init_parameter_lims= [(0, 5),  # Beta0, These are the bounds of the initial guess of the parameters.
                      (0, 0.1),  # beta1, dependency on a
                      (0, 0.1),  # beta2, dependency on b
                      (0.05, 0.2),  # mn, minimal value
                      (0, 0.4)]  # amp, amplitude of the response at saturating signal.

state_names = ["A","E","M"] ##these are the names of the states that you want to compare to the data
data_names = ["A","E","M"] ##these are the corresponding names of the columns in your data sheet.

##^^ This is set up such that you can assign multiple states to a given data column
## for example, state_names = ["A","M","ME"]; data_names = ["A","M","M"]

markov_fit = Markov_fit(data_file="data/proportions_data.csv",
                        dynamic_data_file = "data/switching_data_values.csv",
                        results_folder="results",
                        init_parameter_lims=init_parameter_lims,
                        state_names=state_names,
                        data_names=data_names,
                        transitions_possible=transitions_possible,
                        run_params=run_params,
                        opt_params=opt_params,
                        plot_params=plot_params)
# markov_fit.fit()
markov_fit.fit_multiple()

print([np.array(markov_fit.mrkvSs[i].final_vals_dynamic).min() for i in range(len(markov_fit.mrkvSs))])

markov_fit.plot_fits()
markov_fit.plot_transitions()
# fig, ax = plt.subplots(2,4,figsize=(8,4))
# ax = ax.ravel()
# for j, mrkvS in enumerate(markov_fit.mrkvSs):
#     mrkvS.simulate()
#     # for i, data_name in enumerate(markov_fit.data_names):
#     i = 2
#     data_name = data_names[i]
#     pr = mrkvS.final_vals_dynamic[i]
#     # print(pr)
#     # ax[j].scatter(np.arange(len(pr)),pr,label=data_name,color=markov_fit.solid_colours[i],alpha=0.5)
#     pr_real = markov_fit.df_dynamic[data_name].values
#     ax[j].scatter(np.arange(len(pr_real)),(pr_real/100-pr),color=markov_fit.solid_colours[i],alpha=1)
#     # ax[j].scatter(pr_real,pr,color=markov_fit.solid_colours[i],alpha=1)
#
#     # ax[j].legend()
# fig.show()
