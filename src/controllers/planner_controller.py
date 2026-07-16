import src.models.planner as planner_model

class PlannerController:
    """Controller to manage plan creation, updates, deletions, health scores, split bills, and statistics."""
    
    @staticmethod
    def calculate_plan_total(plan_id: int) -> int:
        return planner_model.calculate_plan_total(plan_id)

    @staticmethod
    def create_plan(user_id: int, nama_rencana: str, tanggal: str, jumlah_teman: int, 
                    budget: int, transportasi: str, transport_cost: int, 
                    mood: str = '😐', mood_efek_persen: float = 0.0, status: str = 'draft') -> int:
        return planner_model.create_plan(user_id, nama_rencana, tanggal, jumlah_teman, budget, 
                                         transportasi, transport_cost, mood, mood_efek_persen, status)

    @staticmethod
    def update_plan_details(plan_id: int, nama_rencana: str, tanggal: str, jumlah_teman: int, 
                            budget: int, transportasi: str, transport_cost: int) -> bool:
        return planner_model.update_plan_details(plan_id, nama_rencana, tanggal, jumlah_teman, 
                                                 budget, transportasi, transport_cost)

    @staticmethod
    def update_plan_mood(plan_id: int, mood: str, mood_efek_persen: float) -> bool:
        return planner_model.update_plan_mood(plan_id, mood, mood_efek_persen)

    @staticmethod
    def save_locations_and_items(plan_id: int, data: list[dict]) -> bool:
        return planner_model.save_locations_and_items(plan_id, data)

    @staticmethod
    def get_plan_locations_and_items(plan_id: int) -> list[dict]:
        return planner_model.get_plan_locations_and_items(plan_id)

    @staticmethod
    def get_plan_details(plan_id: int) -> dict | None:
        return planner_model.get_plan_details(plan_id)

    @staticmethod
    def save_split_bill(plan_id: int, total_tagihan: int, jumlah_orang: int, per_orang: int) -> bool:
        return planner_model.save_split_bill(plan_id, total_tagihan, jumlah_orang, per_orang)

    @staticmethod
    def delete_plan(plan_id: int) -> bool:
        return planner_model.delete_plan(plan_id)

    @staticmethod
    def update_plan_status(plan_id: int, status: str) -> bool:
        return planner_model.update_plan_status(plan_id, status)

    @staticmethod
    def get_user_plans(user_id: int, status: str = None) -> list[dict]:
        return planner_model.get_user_plans(user_id, status)

    @staticmethod
    def get_monthly_spending(user_id: int, year_month: str) -> int:
        return planner_model.get_monthly_spending(user_id, year_month)

    @staticmethod
    def calculate_budget_health_score(user_id: int, target_month: str) -> tuple[int, dict]:
        return planner_model.calculate_budget_health_score(user_id, target_month)

    @staticmethod
    def get_saved_budget_health_score(user_id: int, periode: str) -> dict | None:
        return planner_model.get_saved_budget_health_score(user_id, periode)

    @staticmethod
    def save_or_update_health_score(user_id: int, periode: str) -> int:
        return planner_model.save_or_update_health_score(user_id, periode)

    @staticmethod
    def get_stats_data(user_id: int) -> dict:
        return planner_model.get_stats_data(user_id)

    @staticmethod
    def get_split_bill_checklist(plan_id: int) -> list:
        return planner_model.get_split_bill_checklist(plan_id)

    @staticmethod
    def save_split_bill_checklist(plan_id: int, checklist: list) -> bool:
        return planner_model.save_split_bill_checklist(plan_id, checklist)

    @staticmethod
    def get_user_split_bills(user_id: int) -> list[dict]:
        return planner_model.get_user_split_bills(user_id)

    @staticmethod
    def get_split_bill_selected_items(plan_id: int) -> list[int]:
        return planner_model.get_split_bill_selected_items(plan_id)

    @staticmethod
    def save_split_bill_selected_items(plan_id: int, selected_item_ids: list[int]) -> bool:
        return planner_model.save_split_bill_selected_items(plan_id, selected_item_ids)

    @staticmethod
    def get_user_plan_periods(user_id: int) -> list[str]:
        return planner_model.get_user_plan_periods(user_id)
