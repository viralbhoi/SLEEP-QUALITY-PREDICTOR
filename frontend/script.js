async function predict() {
    const resultElement = document.getElementById("result");
    resultElement.innerHTML = "Predicting..."; // Show loading state

    try {
        // Construct payload using explicit DOM targeting
        let payload = {
            Age: Number(document.getElementById("age").value),
            Gender: document.getElementById("gender").value,
            Occupation: document.getElementById("occupation").value,
            Sleep_Duration: Number(document.getElementById("sleep").value),
            Physical_Activity_Level: Number(
                document.getElementById("activity").value,
            ),
            Stress_Level: Number(document.getElementById("stress").value),
            BMI_Category: document.getElementById("bmi").value,
            Heart_Rate: Number(document.getElementById("heart").value),
            Daily_Steps: Number(document.getElementById("steps").value),
            BP_sys: Number(document.getElementById("bps").value),
            BP_dia: Number(document.getElementById("bpd").value),
        };

        // Call the backend API
        let res = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        // Check if the server responded with a success code
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        let data = await res.json();

        // Update UI with the result
        resultElement.innerHTML = `Score: ${data.predicted_sleep_quality} (${data.sleep_status})`;
    } catch (error) {
        console.error("Prediction failed:", error);
        resultElement.innerHTML =
            "Error: Could not connect to the prediction server.";
        resultElement.style.color = "#e53e3e"; // Turn text red on error
    }
}
