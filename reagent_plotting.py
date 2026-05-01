# Function that draws a plot of single reagent's change in time
# Arguments:
#   reagentstates - List of particle counts of a reagent in various points in time.
#   timetable - List of points in time which correspond to values in 'reagentstates'.
#   name - Name of the reagent being considered.
#   file - (optional string) Name of image file to which to draw the plot.
#   labels - (optional dict) A dictionary of label texts. Use '$name$' to insert reagent name.
#       Recognized label keys: title, xaxis, yaxis
def draw_reagent_plot(reagentstates, timetable, name, file=None,
                        labels={"title" : "Number of particles of $name$ in time",
                                        "xaxis" : "Time", "yaxis" : "$name$ particles"}):

    plt.figure(figsize=(800/60, 480/60), dpi=60) # ~WVGA resolution

    # Draw line plot
    plt.plot(timetable, reagentstates)

    # Replace special elements in labels
    labels_repl = {k : v.replace("$name$", name) for k,v in labels.items()}

    # Draw other elements
    plt.suptitle(labels_repl.get("title", ""), fontsize=24)
    plt.xlabel(labels_repl.get("xaxis", ""), fontsize=18)
    plt.ylabel(labels_repl.get("yaxis", ""), fontsize=18)

    # Optionally save to file
    if file:
        plt.savefig(file)


# Function that draws a plot of multiple reagents' change in time
# Arguments:
#   reagentstates - Dict of symbol : states where symbol is string, reagent's symbol and
#       states is a list of particle counts of that reagent in various points in time.
#
#   timetable - List of points in time which correspond to particle counts in values of 'reagentstates'.
#   name - Dict of symbol : name where symbol is string, reagent's symbol and name is a full
#       name of the reagent being considered.
#
#   file - (optional string) Name of image file to which to draw the plot.
#   labels - (optional dict) A dictionary of label texts. Recognized label keys: title, xaxis, yaxis
def draw_bundled_reagent_plot(reagentstates, timetable, names, file=None,
                                labels={"title" : "Number of particles of $name$ in time",
                                        "xaxis" : "Time", "yaxis" : "$name$ particles"}):

    plt.figure(figsize=(800/60, 480/60), dpi=60) # ~WVGA resolution

    # Color and line style options recognized by pyplot
    color_symbols = list("bgrcmyk")
    style_symbols = ['-', '--', '-.', ':']

    # Draw lines
    for idx, reagent in enumerate(reagentstates):
        # Choose line style and color in such way that ensures that every reagent gets a
        # unique combination
        try:
            col = color_symbols[idx % len(color_symbols)]
            style = style_symbols[idx // len(color_symbols)]

        except IndexError: # Too many reagents, too few line styles available
            raise ValueError("Cannot draw bundled plot - too many reagents!")

        plt.plot(timetable, reagentstates[reagent], style+col, label=names[idx])

    # Draw other elements
    plt.legend(loc=2, bbox_to_anchor=(1,1))
    plt.suptitle(labels.get("title", ""), fontsize=24)
    plt.xlabel(labels.get("xaxis", ""), fontsize=18)
    plt.ylabel(labels.get("yaxis", ""), fontsize=18)

    plt.tight_layout() # Ensures that elements do not stick outside the image

    # Optionally save to file
    if file:
        plt.savefig(file)


# Function that generates and saves plots for each variable
def save_plots(output_dir: Path, timetable: list, states: dict, scenario_desc: str,\
                 labels: dict, split: bool):
    while True:
        if split:
            plot_labels = {
                "title": f"Liczba cząsteczek związku $name$ w czasie\n{scenario_desc}",
                "xaxis": "Czas [h]",
                "yaxis": "Liczba cząsteczek $name$",
            }

            for symbol, values in states.items():
                name = labels.get(symbol, symbol)
                file_path = output_dir / f"{symbol}.png"

                draw_reagent_plot(
                    values,
                    timetable,
                    name,
                    file=str(file_path),
                    labels=plot_labels,
                )
            break

        else:
            plot_labels = {
                "title": f"Liczba cząsteczek związków w czasie\n{scenario_desc}",
                "xaxis": "Czas [h]",
                "yaxis": "Liczba cząsteczek związku",
            }

            names = [labels.get(symbol, symbol) for symbol in states]
            file_path = output_dir / f"Scenario.png"

            try:
                draw_bundled_reagent_plot(
                    states,
                    timetable,
                    names,
                    file=str(file_path),
                    labels=plot_labels,
                )
                break

            except ValueError:
                print("Failed to draw bundled plot. Likely cause is too many reagents - try using the --sp
lit-plots option in future.")
                print("Falling back to split plots automatically.")
                split = False
