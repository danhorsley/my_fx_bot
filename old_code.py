    
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

    
    result_avg = sum(results)/len(results)
    result_worst = min(results)
    results_best = max(results)
    scenario_zero = scenarios[0]
