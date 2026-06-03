// -------------------------------------------------
// Исходные данные (жёстко заданы в коде)
// -------------------------------------------------
const grades = [
    { name: "Макар", score: 85 },
    { name: "Денис", score: 92 },
    { name: "Анна",  score: 78 },
    { name: "Даша",  score: 88 },
    { name: "Студент_X", score: 45 }
];

// -------------------------------------------------
// Настройки анализа
// -------------------------------------------------
const PASSING_THRESHOLD = 60;   // минимальный балл для зачёта

// -------------------------------------------------
// Функция анализа успеваемости
// -------------------------------------------------
function analyzeGrades(arr, passing = PASSING_THRESHOLD) {
    if (!Array.isArray(arr) || arr.length === 0) {
        console.log("Массив оценок пуст или не является массивом.");
        return;
    }

    // 1. Сумма, среднее, мин/макс
    const total = arr.reduce((sum, {score}) => sum + score, 0);
    const avg   = (total / arr.length).toFixed(2);

    const best  = arr.reduce((max, cur) => (cur.score > max.score ? cur : max), arr[0]);
    const worst = arr.reduce((min, cur) => (cur.score < min.score ? cur : min), arr[0]);

    // 2. Количество сдавших/не сдавших
    const passed   = arr.filter(({score}) => score >= passing);
    const failed   = arr.filter(({score}) => score <  passing);

    // 3. Списки имён для удобного вывода
    const passedNames   = passed.map(({name}) => name).join(", ");
    const failedNames   = failed.map(({name}) => name).join(", ");

    // -------------------------------------------------
    // Вывод результатов
    // -------------------------------------------------
    console.log("=== Анализ успеваемости ===");
    console.log(`Количество студентов: ${arr.length}`);
    console.log(`Средний балл: ${avg}`);
    console.log(`Лучший результат: ${best.name} (${best.score})`);
    console.log(`Худший результат: ${worst.name} (${worst.score})`);
    console.log(`Порог зачёта: ${passing}`);
    console.log(`Сдали (${passed.length}): ${passedNames || "нет"}`);
    console.log(`Не сдали (${failed.length}): ${failedNames || "нет"}`);
    console.log("==============================");
}

// -------------------------------------------------
// Запуск анализа
// -------------------------------------------------
analyzeGrades(grades);
