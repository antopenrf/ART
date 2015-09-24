def mea_spot(device, freq):
    device.wrt_single_freq(freq)  ##freq in Hz.
    spot_datum = device.ask_spot_data()
    device.wait_opc()
    return spot_datum

                                            

def core111(device, freq, mode = 'terminal', plotter = None):
    x_axis_freq = []
    y_axis_data = []

    
    for each_f in freq:
        x_axis_freq.append(each_f)
        each_f = each_f*1.0e6

        spot_datum = mea_spot(device, each_f)
        y_axis_data.append(spot_datum)

        if mode == 'plotter':
            plotter.drawgraph(x_axis_freq, y_axis_data,)

        elif mode == 'terminal':
            print("Measuring {freq} MHz: {datum} dB \n".format(freq = each_f, datum = spot_datum))

    return x_axis_freq, y_axis_data    
