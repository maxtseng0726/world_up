import { reactive } from "vue";

export const userStore = reactive({
  dailyGoal: localStorage.getItem("dailyGoal"),
  setGoal(mins: string) {
    this.dailyGoal = mins;
    localStorage.setItem("dailyGoal", mins); // Persists across reloads/app restarts
  },
});
