const topicInput = document.getElementById("topicInput");
const generateButton = document.getElementById("generateButton");
const logArea = document.getElementById("logArea");
const resultArea = document.getElementById("resultArea");

const API_URL = "http://127.0.0.1:8000/generate";


function appendLog(message) {
    logArea.textContent += `${message}\n`;
}


function appendArticle(chunk) {
    resultArea.textContent += chunk;
}


function resetPage() {
    logArea.textContent = "";
    resultArea.textContent = "";
}


function setLoading(isLoading) {
    generateButton.disabled = isLoading;
    generateButton.textContent = isLoading ? "生成中..." : "生成文章";
}


function parseSseBlock(block) {
    const lines = block.split(/\r?\n/);

    let eventType = "message";
    let dataText = "";

    for (const line of lines) {
        if (line.startsWith("event:")) {
            eventType = line.slice(6).trim();
        } else if (line.startsWith("data:")) {
            dataText += line.slice(5).trim();
        }
    }

    if (!dataText) {
        return null;
    }

    try {
        const payload = JSON.parse(dataText);
        return {
            eventType,
            message: payload.message ?? "",
        };
    } catch (error) {
        console.error("SSE JSON 解析失败:", error, dataText);
        return null;
    }
}


async function generateArticle() {
    const topic = topicInput.value.trim();

    if (!topic) {
        alert("请输入文章主题");
        return;
    }

    resetPage();
    setLoading(true);
    appendLog("开始请求后端 Agent...");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
            },
            body: JSON.stringify({ topic }),
        });

        if (!response.ok) {
            throw new Error(`HTTP错误: ${response.status}`);
        }

        if (!response.body) {
            throw new Error("当前浏览器不支持流式响应");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();

            if (done) {
                break;
            }

            buffer += decoder.decode(value, { stream: true });

            const blocks = buffer.split(/\n\n/);
            buffer = blocks.pop() || "";

            for (const block of blocks) {
                const event = parseSseBlock(block);

                if (!event) {
                    continue;
                }

                if (event.eventType === "status") {
                    appendLog(event.message);
                } else if (event.eventType === "article") {
                    appendArticle(event.message);
                } else if (event.eventType === "done") {
                    appendLog(event.message);
                } else if (event.eventType === "error") {
                    appendLog(event.message);
                } else {
                    appendLog(event.message);
                }

                await new Promise((resolve) => requestAnimationFrame(resolve));
            }
        }

        if (buffer.trim()) {
            const lastEvent = parseSseBlock(buffer);
            if (lastEvent) {
                if (lastEvent.eventType === "status") {
                    appendLog(lastEvent.message);
                } else if (lastEvent.eventType === "article") {
                    appendArticle(lastEvent.message);
                } else {
                    appendLog(lastEvent.message);
                }
            }
        }
    } catch (error) {
        console.error(error);
        appendLog(`发生错误: ${error.message}`);
    } finally {
        setLoading(false);
    }
}


generateButton.addEventListener("click", generateArticle);

topicInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        generateArticle();
    }
});

appendLog("前端初始化完成");