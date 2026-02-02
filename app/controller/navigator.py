from app.ui.Dashboard_page import Dashboard


class Navigator:
    def main_window_navigator(self, current_window):
        dashboard = Dashboard()
        dashboard.show()
        current_window.close()
        return dashboard