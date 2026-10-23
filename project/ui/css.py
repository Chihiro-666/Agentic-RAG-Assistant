custom_css = """
    :root {
        color-scheme: dark;
        --app-bg: #0b1017;
        --surface: #121b27;
        --surface-raised: #182434;
        --border: #2a3a4e;
        --text: #e8eef7;
        --muted: #a9b8ca;
        --accent: #75aaff;
        --accent-strong: #4f8ff7;
    }

    .progress-text { display: none !important; }
    body, .gradio-container {
        background: var(--app-bg) !important;
        color: var(--text) !important;
        font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Segoe UI", sans-serif !important;
    }
    .gradio-container {
        width: min(1120px, calc(100% - 40px)) !important;
        max-width: 1120px !important;
        margin: 28px auto !important;
    }
    #app-header {
        padding: 24px 28px 18px !important;
        margin-bottom: 18px !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        background: linear-gradient(135deg, #17263a 0%, #121b27 70%) !important;
    }
    #app-header h1 {
        margin: 0 0 8px !important;
        color: #f2f6fc !important;
        font-size: clamp(24px, 3vw, 32px) !important;
        letter-spacing: .02em;
    }
    #app-header p { color: var(--muted) !important; margin: 0 !important; }

    .tabs, .tab-nav { border-color: var(--border) !important; background: transparent !important; }
    button[role="tab"] {
        color: var(--muted) !important;
        border-radius: 10px 10px 0 0 !important;
        transition: color .18s ease, background .18s ease !important;
    }
    button[role="tab"]:hover { color: var(--text) !important; background: #172333 !important; }
    button[role="tab"][aria-selected="true"] {
        color: #f3f7ff !important;
        border-bottom: 2px solid var(--accent) !important;
        background: #152131 !important;
    }
    #doc-management-tab {
        width: 100% !important;
        max-width: 880px !important;
        margin: 0 auto !important;
        padding: 24px !important;
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
        border: 1px solid #72a7ff !important;
    }
    button.primary:hover, .primary:hover { background: #3678e6 !important; transform: translateY(-1px); }
    button.stop, .stop { background: #a94452 !important; color: #fff !important; }
    button.stop:hover, .stop:hover { background: #c14d5c !important; }

    input, textarea, [data-testid="textbox"] textarea {
        background: #0e1621 !important;
        border: 1px solid var(--border) !important;
        border-radius: 11px !important;
        color: var(--text) !important;
        caret-color: var(--accent) !important;
    }
    input::placeholder, textarea::placeholder { color: #90a1b5 !important; opacity: 1 !important; }
    input:focus, textarea:focus {
        border-color: var(--accent) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(117, 170, 255, .17) !important;
    }
    #file-list-box {
        padding: 12px !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        background: #0e1621 !important;
    }
    #file-list-box textarea { border: 0 !important; background: transparent !important; color: var(--text) !important; }

    [data-testid="file-upload"], .file-preview {
        min-height: 190px !important;
        border: 1px dashed #526b89 !important;
        border-radius: 14px !important;
        background: #101a27 !important;
        color: var(--text) !important;
    }
    [data-testid="file-upload"]:hover, .file-preview:hover {
        border-color: var(--accent) !important;
        background: #152235 !important;
    }
    [data-testid="file-upload"] *, .file-preview * { color: var(--text) !important; }

    #chatbot {
        overflow: hidden !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        background: #0e1621 !important;
    }
    #chatbot .message-wrap, #chatbot > div { gap: 12px !important; padding: 18px !important; }
    #chatbot .message, #chatbot .message-row { border-radius: 14px !important; }
    #chatbot .message.bot, #chatbot .message-row.bot, #chatbot [data-testid="bot"] {
        background: #223247 !important;
        border: 1px solid #3a526e !important;
        color: #f2f6fc !important;
    }
    #chatbot .message.bot *, #chatbot .message-row.bot *, #chatbot [data-testid="bot"] * { color: #f2f6fc !important; }
    #chatbot .message.user, #chatbot .message-row.user, #chatbot [data-testid="user"] {
        background: #28599b !important;
        border: 1px solid #4d83c8 !important;
        color: #fff !important;
    }
    #chatbot .message.user *, #chatbot .message-row.user *, #chatbot [data-testid="user"] * { color: #fff !important; }
    #chatbot .bot {
        background: #223247 !important;
        background-color: #223247 !important;
        border-color: #3a526e !important;
        color: #f2f6fc !important;
        opacity: 1 !important;
    }
    #chatbot .bot .prose,
    #chatbot .bot .prose *,
    #chatbot .bot :where(p, li, strong, em, span, h1, h2, h3, h4, blockquote) {
        color: #f2f6fc !important;
        opacity: 1 !important;
    }
    #chatbot .bot .prose a { color: #91c2ff !important; }
    #chatbot .prose.chatbot.md { opacity: 1 !important; }

    #chatbot code, #chatbot pre {
        color: #e7f0ff !important;
        background: #111c2a !important;
        border-color: #34485f !important;
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

    @media (max-width: 640px) {
        .gradio-container { width: calc(100% - 20px) !important; margin: 10px auto !important; }
        #app-header, #doc-management-tab { padding: 16px !important; }
        #chatbot .message-wrap, #chatbot > div { padding: 10px !important; }
    }
"""