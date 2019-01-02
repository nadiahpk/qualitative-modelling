
import matplotlib.pyplot as plt
from matplotlib import gridspec
import csv
import imp


# Define how I want things to be plotted

# experiments I want to plot individually: (name, plot label)
experiments_to_plot = [ ('Raymond','Raymond\n\n\nbaseline\n'), ('Uniform LV','Lotka-\nVolterra\n\ntest 1\n'), ('Efficiency M','skew\ndistn\n\ntest 2\n') ]
experiment_names, experiment_plot_labels = zip(*experiments_to_plot)

# species responses I want plots of: proportion of negative Sij, for all apart from grassland
spp_responses_to_plot = [ 'S neg albatrosses', 'S neg prions', 'S neg burrowSeabirds', 'S neg petrels', 'S neg herbfield', 'S neg macroInverts', 'S neg mice', 'S neg penguins', 'S neg rabbits', 'S neg rats', 'S neg redpolls', 'S neg skuas', 'S neg surfaceSeabirds', 'S neg tussock', 'S zer tussock' ]

# for the body of the publication I want plots of these only
spp_responses_to_plot_pubn = [ 'S neg prions', 'S neg penguins', 'S neg redpolls', 'S neg skuas']
#spp_responses_to_plot_pubn = [ 'S neg penguins', 'S neg macroInverts', 'S neg redpolls', 'S neg skuas']



# Get species labels, the collated results, and put them into a useful form

# get species labels
f = open('macq1.py') # where the dictionary defining the foodweb we're using is defined
data = imp.load_source('data', '', f)
f.close() # now have data.pretty_names: key is species and value is the full name for the species

# get the results from the csv file
fIn = open('collate_all.csv') # open csv
csv_f = csv.reader(fIn) # get row iterator
header = next(csv_f) # header info
results = { row[0]: [ int(x) for x in row[1:]] for row in csv_f } # recreate dictionary
fIn.close()

# put the results in two separate dictionaries
stability_results = dict()
other_results = dict()
for experiment_name, data_list in results.items():

    if experiment_name[:22] == 'Difficult stability M ':

        Ef = -float(experiment_name.split()[-1])
        stability_results[Ef] = data_list

    else:

        other_results[experiment_name] = data_list



# Organise rejections result by experiment name

rejections_by_experiment = dict()

for (experiment_name,experiment_plot_label) in experiments_to_plot:

    data_list = results[experiment_name]
    rejections_by_experiment[experiment_name] = data_list[1]/data_list[0]

rejections_by_experiment['Difficult stability'] = list()

for Ef, data_list in stability_results.items():

    rejections_by_experiment['Difficult stability'].append( ( Ef, data_list[1]/data_list[0] ) )



# Organise the species-response results by species

results_by_spp_response = dict() # proportion positive response to rabbit control

for spp_response in spp_responses_to_plot:

    # ready the dictionary entries
    results_by_spp_response[spp_response] = dict()

    idx = header.index(spp_response) - 1

    for (experiment_name,experiment_plot_label) in experiments_to_plot:

        data_list = results[experiment_name]
        results_by_spp_response[spp_response][experiment_name] = data_list[idx]/data_list[0]

    results_by_spp_response[spp_response]['Difficult stability'] = list()
    for Ef, data_list in stability_results.items():
        results_by_spp_response[spp_response]['Difficult stability'].append( (Ef,data_list[idx]/data_list[0]) )



# Create each species-responses plots

if True:

    for spp_response, propn_pos in results_by_spp_response.items():
    #spp_response = 'S neg penguins'
    #propn_pos = results_by_spp_response[spp_response]
    #if True:

        f, (other_ax, stability_ax) = plt.subplots( 1, 2, figsize=(9,2.5) )
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 3])

        spp = spp_response.split()[-1]
        y_label = data.pretty_names[spp]

        x_vals = list(range(len(experiments_to_plot)))
        y_vals = [ propn_pos[experiment_name] for experiment_name in experiment_names ]

        other_ax = plt.subplot(gs[0])
        other_ax.scatter( x_vals, y_vals, color='black' )
        other_ax.set_ylabel( y_label )
        other_ax.set_ylim( (-0.05,1.05) )
        other_ax.set_yticks( (0, 0.25, 0.5, 0.75, 1) )
        other_ax.set_xlabel( ' ' )
        other_ax.set_xticks(x_vals)
        other_ax.set_xticklabels( ('baseline', 'test 1', 'test 2') )
        other_ax.grid(True)
        other_ax.set_axisbelow(True)

        x_vals, y_vals = zip(*propn_pos['Difficult stability'])

        stability_ax = plt.subplot(gs[1])
        stability_ax.scatter( x_vals, y_vals, color='black' )
        stability_ax.set_xlabel( ' expected magnitude of consumer diagonal element, test 3 ' )
        stability_ax.set_ylim( (-0.05,1.05) )
        stability_ax.tick_params(labelleft='off', left='off', right='on')
        stability_ax.grid(True)
        stability_ax.set_axisbelow(True)

        plt.tight_layout(w_pad=0)
        plt.savefig('response_' + spp + '.pdf')
        plt.close()


# Create the average number of rejected draws per accepted community matrix plot

if True:

    f, (other_ax, stability_ax) = plt.subplots( 1, 2, sharey=True, figsize=(9,2.5) )
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 3])

    y_label = 'avg. no rejected draws\nper plausible matrix'

    x_vals = list(range(len(experiments_to_plot)))
    y_vals = [ rejections_by_experiment[experiment_name] for experiment_name in experiment_names ]

    other_ax = plt.subplot(gs[0])
    other_ax.scatter( x_vals, y_vals, color='red' )
    other_ax.set_ylabel( y_label )
    other_ax.set_yscale('log')
    other_ax.set_xlabel( ' ' )
    other_ax.set_xticks(x_vals)
    other_ax.set_xticklabels(experiment_plot_labels)
    other_ax.grid(True)
    other_ax.set_axisbelow(True)

    x_vals, y_vals = zip(*rejections_by_experiment['Difficult stability'])

    stability_ax = plt.subplot(gs[1], sharey=other_ax)
    stability_ax.scatter( x_vals, y_vals, color='red' )
    stability_ax.set_xlabel( ' test 3, expected magnitude of consumer diagonal element ' )
    stability_ax.set_yscale('log')
    stability_ax.tick_params(labelleft='off', left='off', right='on')
    stability_ax.grid(True)
    stability_ax.set_axisbelow(True)

    plt.tight_layout(w_pad=0)
    plt.savefig('rejections.pdf')
    plt.close()
    #plt.show()


# Create the plot for the body of the publication

if True:

    if False:

        no_rows = len(spp_responses_to_plot_pubn) + 1
        f, ax = plt.subplots( no_rows, 2, figsize=(9,no_rows*2.0) )
        gs = gridspec.GridSpec(no_rows, 2, width_ratios=[1, 3])

        # The rejections count plot

        y_label = 'avg. no rejected draws\nper plausible matrix'

        x_vals = list(range(len(experiments_to_plot)))
        y_vals = [ rejections_by_experiment[experiment_name] for experiment_name in experiment_names ]

        ax[0][0] = plt.subplot(gs[0,0])
        ax[0][0].scatter( x_vals, y_vals, color='red' )
        ax[0][0].set_ylabel( y_label, labelpad=15 )
        ax[0][0].set_yscale('log')
        ax[0][0].grid(True)
        ax[0][0].set_axisbelow(True)
        ax[0][0].tick_params(labelbottom='off')

        x_vals, y_vals = zip(*rejections_by_experiment['Difficult stability'])

        ax[0][1] = plt.subplot(gs[0,1], sharey=ax[0][0])
        ax[0][1].scatter( x_vals, y_vals, color='red' )
        ax[0][1].set_yscale('log')
        ax[0][1].tick_params(labelleft='off', labelbottom='off', left='off', right='on')
        ax[0][1].grid(True)
        ax[0][1].set_axisbelow(True)

        j = 1

    else:

        no_rows = len(spp_responses_to_plot_pubn)
        f, ax = plt.subplots( no_rows, 2, figsize=(9,no_rows*2.0) )
        gs = gridspec.GridSpec(no_rows, 2, width_ratios=[1, 3])

        j = 0


    # Each of the species responses

    for idx, spp_response in enumerate(spp_responses_to_plot_pubn):

        propn_pos = results_by_spp_response[spp_response]

        spp = spp_response.split()[-1]
        y_label = data.pretty_names[spp]

        x_vals = list(range(len(experiments_to_plot)))
        y_vals = [ propn_pos[experiment_name] for experiment_name in experiment_names ]

        ax[idx+j][0] = plt.subplot(gs[idx+j,0], sharex=ax[0][0])
        ax[idx+j][0].scatter( x_vals, y_vals, color='black' )
        ax[idx+j][0].set_ylabel( '\n\n' + y_label )
        ax[idx+j][0].set_ylim( (-0.05,1.05) )
        ax[idx+j][0].grid(True)
        ax[idx+j][0].set_axisbelow(True)
        ax[idx+j][0].tick_params(labelbottom='off')

        x_vals, y_vals = zip(*propn_pos['Difficult stability'])

        ax[idx+j][1] = plt.subplot(gs[idx+j,1], sharex=ax[0][1], sharey=ax[idx+j][0])
        ax[idx+j][1].scatter( x_vals, y_vals, color='black' )
        ax[idx+j][1].set_ylim( (-0.05,1.05) )
        ax[idx+j][1].tick_params(labelleft='off', left='off', labelbottom='off', right='on')
        ax[idx+j][1].grid(True)
        ax[idx+j][1].set_axisbelow(True)

    # put the labels back on the last x-axis
    ax[-1][0].set_xlabel( ' ' )
    x_vals = list(range(len(experiments_to_plot)))
    ax[-1][0].set_xticks(x_vals)
    ax[-1][0].set_xticklabels(experiment_plot_labels)
    ax[-1][0].tick_params(labelbottom='on')
    ax[-1][1].set_xlabel( ' expected magnitude of consumer diagonal element\n\n "strength" of stability constraint, test 3 ' )
    ax[-1][1].tick_params(labelleft='off', left='off', labelbottom='on', right='on')

    f.text(0.02, 0.45, 'proportion of positive responses', ha='center', va='center', rotation='vertical')
    f.text(0.5, 0.01, '', ha='center', va='center')

    '''
    f.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.grid(False)
    plt.ylabel("proportion of positive responses", labelpad=30)
    '''

    plt.tight_layout(w_pad=0)
    plt.savefig('selected.pdf')
    plt.close()
    #plt.show()
