import { ref, computed } from "vue";

export function useTimer(getInitialMinutes: () => number) {
    // Total time in seconds
    const totalSeconds = computed(() => getInitialMinutes() * 60);
    const timeLeft = ref(totalSeconds.value);
    let timerInterval: number | null = null;
    const isRunning = ref(false);

    // Percentage of pastime
    const progressPercentage = computed(() => {
        const elapsed = totalSeconds.value - timeLeft.value;
        const pct = (elapsed / totalSeconds.value) * 100;
        return Math.min(Math.max(pct, 0), 100);
    });

    // 開始計時
    const startTimer = (onComplete?: () => void) => {
        if (isRunning.value || timeLeft.value <= 0) return;
        isRunning.value = true;

        timerInterval = window.setInterval(() => {
            if (timeLeft.value > 0) {
                timeLeft.value--;
            } else {
                stopTimer();
                if (onComplete) onComplete();
            }
        }, 1000);
    };

    // 暫停計時
    const stopTimer = () => {
        if (timerInterval !== null) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        isRunning.value = false;
    };

    // 當目標分鐘數改變時，同步更新時間
    const syncWithGoal = () => {
        timeLeft.value = totalSeconds.value;
    };

    return {
        timeLeft,
        isRunning,
        progressPercentage,
        startTimer,
        stopTimer,
        syncWithGoal,
    };
}