custom_css = """
    :root {
        color-scheme: light dark;
        --app-bg: #f3f6fb;
        --surface: #ffffff;
        --surface-raised: #eaf0f7;
        --surface-hover: #e8eff8;
        --border: #d4deea;
        --text: #1c2938;
        --muted: #526174;
        --accent: #3478d4;
        --accent-strong: #2868c0;
        --header-start: #e5efff;
        --header-end: #ffffff;
        --input-bg: #ffffff;
        --upload-bg: #f8fafd;
        --chat-bg: #f7f9fc;
        --bot-bg: #ffffff;
        --bot-border: #d5deea;
        --bot-text: #1d2938;
        --user-bg: #dcecff;
        --user-border: #bbd5f3;
        --user-text: #172b45;
        --code-bg: #edf2f8;
        --code-text: #22334a;
        --link: #175fb3;
        --focus-ring: rgba(52, 120, 212, .2);
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --app-bg: #0b1017;
            --surface: #121b27;
            --surface-raised: #182434;
            --surface-hover: #202f42;
            --border: #2a3a4e;
            --text: #e8eef7;
            --muted: #b8c5d5;
            --accent: #86b6ff;
            --accent-strong: #4f8ff7;
            --header-start: #17263a;
            --header-end: #121b27;
            --input-bg: #0e1621;
            --upload-bg: #101a27;
            --chat-bg: #0e1621;
            --bot-bg: #223247;
            --bot-border: #3a526e;
            --bot-text: #f2f6fc;
            --user-bg: #28599b;
            --user-border: #4d83c8;
            --user-text: #ffffff;
            --code-bg: #111c2a;
            --code-text: #e7f0ff;
            --link: #91c2ff;
            --focus-ring: rgba(117, 170, 255, .24);
        }
    }

    .progress-text { display: none !important; }

    body, .gradio-container {
        background: var(--app-bg) !important;
        color: var(--text) !important;
        font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Segoe UI", sans-serif !important;
    }
    .gradio-container {
        width: min(1600px, calc(100% - 40px)) !important;
        max-width: 1600px !important;
        margin: clamp(12px, 2vh, 24px) auto !important;
    }

    #app-header {
        padding: clamp(18px, 3vw, 28px) !important;
        margin-bottom: clamp(12px, 2vw, 20px) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        background: linear-gradient(135deg, var(--header-start), var(--header-end)) !important;
    }
    #app-header h1 {
        margin: 0 0 8px !important;
        color: var(--text) !important;
        font-size: clamp(23px, 3vw, 32px) !important;
        letter-spacing: .02em;
    }
    #app-header p { color: var(--muted) !important; margin: 0 !important; }

    .tabs, .tab-nav { border-color: var(--border) !important; background: transparent !important; }
    .tab-nav { overflow-x: auto !important; }
    button[role="tab"] {
        color: var(--muted) !important;
        border-radius: 10px 10px 0 0 !important;
        transition: color .18s ease, background .18s ease !important;
    }
    button[role="tab"]:hover { color: var(--text) !important; background: var(--surface-hover) !important; }
    button[role="tab"][aria-selected="true"] {
        color: var(--text) !important;
        border-bottom: 2px solid var(--accent) !important;
        background: var(--surface) !important;
    }

    #doc-management-tab {
        width: 100% !important;
        max-width: 880px !important;
        margin: 0 auto !important;
        padding: clamp(16px, 3vw, 28px) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0 0 16px 16px !important;
        background: var(--surface) !important;
    }
    #doc-management-tab h2 { color: var(--text) !important; margin: 8px 0 10px !important; }
    #doc-management-tab p { color: var(--muted) !important; line-height: 1.7 !important; }

    button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: background .18s ease, transform .18s ease !important;
    }
    button.primary, .primary {
        background: var(--accent-strong) !important;
        color: #fff !important;
        border: 1px solid var(--accent) !important;
    }
    button.primary:hover, .primary:hover { filter: brightness(1.08); transform: translateY(-1px); }
    button.stop, .stop { background: #a94452 !important; color: #fff !important; }
    button.stop:hover, .stop:hover { background: #c14d5c !important; }

    input, textarea, [data-testid="textbox"] textarea {
        background: var(--input-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 11px !important;
        color: var(--text) !important;
        caret-color: var(--accent) !important;
    }
    input::placeholder, textarea::placeholder { color: var(--muted) !important; opacity: 1 !important; }
    input:focus, textarea:focus {
        border-color: var(--accent) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px var(--focus-ring) !important;
    }
    #file-list-box {
        padding: 12px !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        background: var(--input-bg) !important;
    }
    #file-list-box textarea { border: 0 !important; background: transparent !important; color: var(--text) !important; }

    [data-testid="file-upload"], .file-preview {
        min-height: 180px !important;
        border: 1px dashed var(--border) !important;
        border-radius: 14px !important;
        background: var(--upload-bg) !important;
        color: var(--text) !important;
    }
    [data-testid="file-upload"]:hover, .file-preview:hover {
        border-color: var(--accent) !important;
        background: var(--surface-hover) !important;
    }
    [data-testid="file-upload"] *, .file-preview * { color: var(--text) !important; }

    #chatbot {
        height: calc(100vh - 250px) !important;
        min-height: 420px !important;
        overflow: hidden !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        background: var(--chat-bg) !important;
    }
    #chatbot .message-wrap, #chatbot > div { gap: 12px !important; padding: clamp(10px, 2vw, 20px) !important; }
    #chatbot .message, #chatbot .message-row { border-radius: 14px !important; }

    #chatbot .bot {
        background: var(--bot-bg) !important;
        background-color: var(--bot-bg) !important;
        border: 1px solid var(--bot-border) !important;
        color: var(--bot-text) !important;
        opacity: 1 !important;
    }
    #chatbot .bot .prose,
    #chatbot .bot .prose *,
    #chatbot .bot :where(p, li, strong, em, span, h1, h2, h3, h4, blockquote) {
        color: var(--bot-text) !important;
        opacity: 1 !important;
    }
    #chatbot .bot .prose a { color: var(--link) !important; }
    #chatbot .prose.chatbot.md { opacity: 1 !important; }
    #chatbot .user {
        background: var(--user-bg) !important;
        background-color: var(--user-bg) !important;
        border: 1px solid var(--user-border) !important;
        color: var(--user-text) !important;
    }
    #chatbot .user .prose,
    #chatbot .user .prose *,
    #chatbot .user :where(p, li, strong, em, span, h1, h2, h3, h4, blockquote) {
        color: var(--user-text) !important;
        opacity: 1 !important;
    }
    #chatbot code, #chatbot pre {
        color: var(--code-text) !important;
        background: var(--code-bg) !important;
        border-color: var(--border) !important;
    }

    form:has(textarea[placeholder="输入问题后按 Enter 发送"]) {
        gap: 10px !important;
        padding: 10px !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        background: var(--surface) !important;
    }
    form:has(textarea[placeholder="输入问题后按 Enter 发送"]) textarea {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        color: var(--text) !important;
    }
    form:has(textarea[placeholder="输入问题后按 Enter 发送"]) button { border-radius: 9px !important; }

    h1, h2, h3, h4, h5, h6, label { color: var(--text) !important; }
    p, small { color: var(--muted); }
    .progress-bar-wrap { border-radius: 8px !important; background: var(--surface-raised) !important; }
    .progress-bar { border-radius: 8px !important; background: var(--accent) !important; }
    footer { display: none !important; }

    @media (max-width: 760px) {
        .gradio-container { width: calc(100% - 24px) !important; margin: 12px auto !important; }
        #chatbot { height: 65vh !important; min-height: 55vh !important; }
        #chatbot .message-wrap, #chatbot > div { padding: 12px !important; }
        #chatbot .bot, #chatbot .user { max-width: 92% !important; }
    }

    @media (max-width: 480px) {
        .gradio-container { width: calc(100% - 16px) !important; margin: 8px auto !important; }
        #app-header { padding: 16px !important; border-radius: 14px !important; }
        #doc-management-tab { padding: 14px !important; }
        #chatbot { min-height: 60vh !important; border-radius: 12px !important; }
        #chatbot .message-wrap, #chatbot > div { padding: 8px !important; }
        #chatbot .bot, #chatbot .user { max-width: 96% !important; }
        form:has(textarea[placeholder="输入问题后按 Enter 发送"]) { padding: 6px !important; gap: 6px !important; }
    }
"""