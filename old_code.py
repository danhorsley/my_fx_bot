    
    #creating plot of simulations
    # plt.clf()
    # plt.plot(mc.iloc[:, :10])
    # strFile = 'crawler/static/images/new_plot2.png'
    # if os.path.isfile(strFile):
    #     os.remove(strFile)
    # plt.savefig(strFile)

            # s_slice = rg[-s:]
        # m_slice = rg[-m:]
        # l_slice = rg[-l:]
        # slices = [s_slice, m_slice, l_slice]


    # plt.clf()
    # data_color = [x / max(results) for x in results]
    # my_cmap = plt.cm.get_cmap('RdBu')
    # colors = my_cmap(data_color)
    # plt.bar(x=my_dict.keys(),height = my_dict.values(),width=0.8,color=colors)
    # strFile2 = 'crawler/static/images/bar_plot.png'
    # if os.path.isfile(strFile2):
    #     os.remove(strFile2)
    # plt.savefig(strFile2)
    #default font is Inconsolata

    
@main.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


    
    result_avg = sum(results)/len(results)
    result_worst = min(results)
    results_best = max(results)
    scenario_zero = scenarios[0]
