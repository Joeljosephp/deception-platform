from django.urls import path

from .views import (
    SecurityEventListCreateView,
    AIAnalysisView,
    DashboardStatsView,
    AttackerSimulationView,
    AttackerListView,
)


urlpatterns = [

    path(
        "events/",
        SecurityEventListCreateView.as_view(),
        name="events"
    ),

    path(
        "analysis/",
        AIAnalysisView.as_view(),
        name="analysis"
    ),

    path(
        "dashboard/",
        DashboardStatsView.as_view(),
        name="dashboard-stats"
    ),

    path(
        "attackers/<int:attacker_id>/simulate/",
        AttackerSimulationView.as_view(),
        name="attacker-simulate"
    ),

    path(
    "attackers/",
    AttackerListView.as_view(),
    name="attackers-list"
),

]