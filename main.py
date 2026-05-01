import next_reaction as NR
import reagent_plotting as rplt
import config_loader as cl

import argparse
import csv
from pathlib import Path


# Function that saves simulation results to CSV file
def save_csv(path: Path, timetable, states: dict):
    symbols = list(states.keys())

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Header: time + variable names
        writer.writerow(["time", *symbols])

        # Write rows: time + values of all variables
        for i, t in enumerate(timetable):
            row = [t] + [states[symbol][i] for symbol in symbols]
            writer.writerow(row)


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

                rplt.draw_reagent_plot(
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
                rplt.draw_bundled_reagent_plot(
                    states,
                    timetable,
                    names,
                    file=str(file_path),
                    labels=plot_labels,
                )
                break

            except ValueError:
                print("Failed to draw bundled plot. Likely cause is too many reagents - try using the --split-plots option in future.")
                print("Falling back to split plots automatically.")
                split = False


# Function that runs simulation for a single scenario
# builds model, runs RK4, saves plots and optionally CSV
def run_single_scenario(config: dict, scenario: str | None, output_dir: Path,\
                        write_csv: bool, split : bool):
    model, start, step, timespan, labels, description = cl.build_inputs(config, scenario)

    # Run RK4 simulation
    # TODO: Change this to Next Reaction
    #timetable, states = rk4(model, start, step, timespan)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save plots
    save_plots(output_dir, timetable, states, description, labels, split)

    # Optionally save CSV
    if write_csv:
        save_csv(output_dir / "results.csv", timetable, states)

    scenario_text = scenario if scenario else "default"
    print(f"Zakończono scenariusz: {scenario_text}")
    if description:
        print(f"Opis: {description}")
    print(f"Wyniki zapisano w: {output_dir}")


# Function that parses CLI arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="Symulacja modelu biologicznego metodą Rungego-Kutty IV"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Ścieżka do pliku YAML z modelem",
    )

    parser.add_argument(
        "--scenario",
        default=None,
        help="Nazwa scenariusza z YAML, np. A, B, C, D albo all",
    )

    parser.add_argument(
        "--out",
        default="results",
        help="Folder na wyniki",
    )

    parser.add_argument(
        "--csv",
        action="store_true",
        help="Zapisz wyniki także do pliku CSV",
    )

    parser.add_argument(
        "--split-plots",
        action="store_true",
        dest="split",
        help="Zamiast pojedynczego wykresu dla wszystkich związków w scenariuszu, wygeneruj oddzielny wykres dla każdego związku. W niektórych przypadkach (zbyt wiele związków, by zmieściłysię na wykresie) użycie tej opcji może być niezbędne (w przeciwnym razie wystąpią błędy).",
    )

    return parser.parse_args()


# Main function controlling program execution
def main():
    args = parse_args()

    # Load configuration from YAML
    config = cl.load_config(args.config)
    output_root = Path(args.out)

    # By default run all scenarios
    if not args.scenario:
        args.scenario = "all"

    # Run all scenarios
    if args.scenario.lower() == "all":
        names = cl.scenario_names(config)

        if not names:
            raise ValueError("W pliku YAML nie ma żadnych scenariuszy.")

        for scenario in names:
            run_single_scenario(
                config=config,
                scenario=scenario,
                output_dir=output_root / scenario,
                write_csv=args.csv,
                split=args.split
            )

    # Run single scenario
    else:
        run_single_scenario(
            config=config,
            scenario=args.scenario,
            output_dir=output_root,
            write_csv=args.csv,
            split=args.split
        )


if __name__ == "__main__":
    main()
