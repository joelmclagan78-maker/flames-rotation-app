import flet as ft
import asyncio

async def main(page: ft.Page):
    page.title = "Flames Rotation Master"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.bgcolor = "black"
    
    # Official Roster
    initial_roster = "Xavier, Max, Jordan, Bertrand, Tyler, Jerry, Alex, Vinnie"
    players = {}
    state = {"running": False, "time": 1200, "half": "1st Half"}

    timer_display = ft.Text("20:00", size=70, color="orange", weight="bold")
    half_label = ft.Text("1st HALF", size=20, weight="bold", color="blue")

    def build_roster(names_str):
        nonlocal players
        names = [n.strip() for n in names_str.split(",") if n.strip()]
        players = {name: {"h1_mins": 0, "h2_mins": 0, "status": "Bench", "target": 12} for name in names}

    build_roster(initial_roster)

    async def tick():
        while True:
            if state["running"] and state["time"] > 0:
                state["time"] -= 1
                m, s = divmod(state["time"], 60)
                timer_display.value = "%02d:%02d" % (m, s)
                for name, data in players.items():
                    if data["status"] == "On Court":
                        if state["half"] == "1st Half": data["h1_mins"] += 1
                        else: data["h2_mins"] += 1
                await render_players()
                page.update()
            await asyncio.sleep(1)

    player_list = ft.ListView(expand=True, spacing=10, padding=10)

    async def render_players():
        player_list.controls.clear()
        for name, data in players.items():
            is_on_court = data["status"] == "On Court"
            bg = "#2e7d32" if is_on_court else "#222222"
            total_secs = data["h1_mins"] if state["half"] == "1st Half" else data["h2_mins"]
            m, s = divmod(total_secs, 60)
            
            if data["status"] == "Bench":
                # High Visibility Bench Label
                content = ft.Row([
                    ft.Text("BENCH", weight="bold", size=40, color="white", expand=True),
                    ft.Text(name.upper(), size=18, weight="bold", color="orange")
                ], alignment="center")
            else:
                content = ft.Row([
                    ft.Column([ft.Text(name, weight="bold", size=22), ft.Text("Goal: %sm" % data['target'], size=12)], expand=True),
                    ft.Text("%sm %02ds" % (m, s), size=22, weight="bold")
                ])
            player_list.controls.append(ft.Container(content=content, padding=15, border_radius=12, bgcolor=bg, on_click=toggle, data=name))

    async def toggle(e):
        p_name = e.control.data
        players[p_name]["status"] = "On Court" if players[p_name]["status"] == "Bench" else "Bench"
        await render_players()
        page.update()

    roster_field = ft.TextField(label="Edit Names", value=initial_roster, multiline=True)
    async def lock(e):
        build_roster(roster_field.value)
        setup_view.visible, game_view.visible = False, True
        await render_players()
        page.update()

    setup_view = ft.Container(content=ft.Column([ft.Text("ROSTER", size=20, weight="bold"), roster_field, ft.TextButton("LOCK & START", on_click=lock)]), padding=20)
    game_view = ft.Column([ft.Row([half_label]), timer_display, ft.Row([ft.TextButton("START", on_click=lambda _: state.update({"running": True})), ft.TextButton("STOP", on_click=lambda _: state.update({"running": False}))], alignment="center")], visible=False)

    await render_players()
    page.add(setup_view, ft.Container(content=game_view), ft.Container(content=player_list, expand=True))
    asyncio.create_task(tick())

# Explicit desktop execution
if __name__ == "__main__":
import os
port = int(os.getenv("PORT", 8501))
ft.app(target=main, view=None, port=port)


