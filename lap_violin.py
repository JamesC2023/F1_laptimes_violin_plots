import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import fastf1
import fastf1.plotting
import logging
import matplotlib.patches as mpatches

def _suppress_fastf1_warnings():
    for logger_name in ['fastf1', 'fastf1.core', 'fastf1._api']:
        logging.getLogger(logger_name).setLevel(logging.ERROR)

def drivers_lap_violin(race, year=2025, session="R", drivers="top10"):
    _suppress_fastf1_warnings()
    race_session=fastf1.get_session(year, race, session)
    race_session.load()
    laps=race_session.laps
    laps.LapTime = laps.LapTime / np.timedelta64(1,"s")
    laps = laps[laps["PitInTime"].isnull()]
    laps = laps[laps["PitOutTime"].isnull()]
    laps = laps.query("TrackStatus=='1'")
    laps = laps.query("LapNumber != 1")
    results = race_session.results.loc[:,"Abbreviation"]
    if drivers != "all":
        if drivers == "top5":
            drivers = results[:5]
        elif drivers == "top10":
            drivers = results[:10]
        laps = laps[laps["Driver"].isin(drivers)]
    else:
        drivers = results
    driver_colors = {driver : fastf1.plotting.get_driver_color(driver, race_session) for driver in drivers}
    tyre_colors = {compound.upper() : fastf1.plotting.get_compound_color(compound, race_session) for compound in laps.loc[:,"Compound"].unique()}
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    fig.set_figheight(0.8*len(drivers))
    fig.set_figwidth(8.3)
    sns.violinplot(data=laps, y="Driver", x="LapTime", hue="Driver", order=drivers, palette=driver_colors, legend=False, inner=None, linewidth=0, ax=ax)
    sns.swarmplot(data=laps, y="Driver", x="LapTime", hue="Compound", order=drivers, palette=tyre_colors, size=4, legend=False, ax=ax)
    ax.set_title(f"{year} {race_session.event.EventName} {race_session.event.get_session_name(session)} lap times")
    ax.set_xlabel("Lap time (seconds)")
    ax.set_ylabel("")
    handles = [mpatches.Patch(color=tyre_colors[compound], label=compound) for compound in laps["Compound"].unique()]
    ax.legend(handles=handles, loc=1, title="Tyre compound")
    plt.show()

def teams_lap_violin(race, year=2025, session="R", teams="all"):
    _suppress_fastf1_warnings()
    race_session=fastf1.get_session(year, race, session)
    race_session.load()
    laps=race_session.laps
    laps.LapTime = laps.LapTime / np.timedelta64(1,"s")
    laps = laps[laps["PitInTime"].isnull()]
    laps = laps[laps["PitOutTime"].isnull()]
    laps = laps.query("TrackStatus=='1'")
    laps = laps.query("LapNumber != 1")
    if teams != "all":
        if teams == "big4":
            teams = ["McLaren", "Ferrari", "Red Bull Racing", "Mercedes"]
        laps = laps[laps["Team"].isin(teams)]
    else:
        teams = race_session.results.loc[:,"TeamName"].unique()
    team_colors = {team : fastf1.plotting.get_team_color(team, race_session) for team in teams}
    tyre_colors = {compound.upper() : fastf1.plotting.get_compound_color(compound, race_session) for compound in laps.loc[:,"Compound"].dropna().unique()}
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    fig.set_figheight(1.6*len(teams))
    fig.set_figwidth(8.3)
    sns.violinplot(data=laps, y="Team", x="LapTime", hue="Team", order=teams, palette=team_colors, legend=False, inner=None, linewidth=0, ax=ax)
    sns.swarmplot(data=laps, y="Team", x="LapTime", hue="Compound", order=teams, palette=tyre_colors, size=4, legend=False, ax=ax)
    ax.set_title(f"{year} {race_session.event.EventName} {race_session.event.get_session_name(session)} lap times")
    ax.set_xlabel("Lap time (seconds)")
    ax.set_ylabel("")
    handles = [mpatches.Patch(color=tyre_colors[compound], label=compound) for compound in laps["Compound"].unique()]
    ax.legend(handles=handles, loc=1, title="Tyre compound")
    plt.show()