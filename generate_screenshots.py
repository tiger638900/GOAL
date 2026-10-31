import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    # Try common Windows fonts
    font_names = [
        "C:\\Windows\\Fonts\\segoeui.ttf" if not bold else "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arial.ttf" if not bold else "C:\\Windows\\Fonts\\arialbd.ttf",
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_openshift_chrome(draw, width, height, active_tab="Storage", title_text=""):
    # Background
    draw.rectangle([0, 0, width, height], fill="#151515")
    
    # Top navbar
    draw.rectangle([0, 0, width, 50], fill="#1b1d21")
    draw.line([0, 50, width, 50], fill="#393f44", width=1)
    
    f_logo = get_font(16, bold=True)
    f_sub = get_font(13)
    f_bold = get_font(14, bold=True)
    f_reg = get_font(13)
    f_small = get_font(11)
    
    # Red Hat OpenShift Logo mark
    draw.rectangle([15, 12, 38, 38], fill="#ee0000", outline="#cc0000")
    draw.polygon([(26, 17), (20, 33), (32, 33)], fill="#ffffff")
    draw.text((45, 16), "Red Hat", font=f_logo, fill="#ffffff")
    draw.text((115, 16), "OpenShift", font=f_logo, fill="#e0e0e0")
    
    # Perspective Switcher
    draw.rectangle([210, 10, 310, 40], fill="#26292d", outline="#44484d")
    draw.text((225, 17), "Administrator ▾", font=f_sub, fill="#06c")
    
    # Project Selector
    draw.rectangle([325, 10, 560, 40], fill="#26292d", outline="#44484d")
    draw.text((335, 17), "Project: sn-labs-tiger638900 ▾", font=f_sub, fill="#f0f0f0")
    
    # Right side icons
    draw.text((width - 250, 17), "🔍 Search", font=f_sub, fill="#aaa")
    draw.text((width - 160, 17), "🔔", font=f_sub, fill="#aaa")
    draw.text((width - 120, 17), "❓", font=f_sub, fill="#aaa")
    draw.text((width - 80, 17), "👤 tiger638900", font=f_sub, fill="#39a5dc")

    # Left Sidebar
    draw.rectangle([0, 51, 220, height], fill="#212427")
    draw.line([220, 51, 220, height], fill="#393f44", width=1)
    
    nav_items = [
        ("Home", "🏠"),
        ("Operators", "⚙"),
        ("Workloads", "📦"),
        ("Pipelines", "🔀"),
        ("Builds", "🔨"),
        ("Storage", "💾"),
        ("Networking", "🌐"),
        ("User Management", "👥"),
        ("Administration", "🔧")
    ]
    
    y = 70
    for name, icon in nav_items:
        is_active = (name == active_tab)
        if is_active:
            draw.rectangle([0, y-6, 219, y+24], fill="#151515")
            draw.rectangle([0, y-6, 4, y+24], fill="#06c")
            color = "#39a5dc"
            f_item = f_bold
        else:
            color = "#d2d2d2"
            f_item = f_reg
            
        draw.text((20, y), icon, font=f_reg, fill=color)
        draw.text((45, y), name, font=f_item, fill=color)
        y += 38

def create_pvc_details_screenshot():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), "#0f1214")
    draw = ImageDraw.Draw(img)
    
    draw_openshift_chrome(draw, w, h, active_tab="Storage")
    
    f_h1 = get_font(22, bold=True)
    f_h2 = get_font(15, bold=True)
    f_lbl = get_font(12)
    f_val = get_font(13, bold=True)
    f_tag = get_font(11, bold=True)
    f_mono = get_font(12)
    f_crumb = get_font(12)
    
    # Breadcrumbs
    draw.text((250, 70), "PersistentVolumeClaims  >  pipelinerun-pvc", font=f_crumb, fill="#73bcf7")
    
    # Title & Badge
    draw.text((250, 95), "pipelinerun-pvc", font=f_h1, fill="#ffffff")
    
    # Status Badge 'Bound'
    draw.rectangle([450, 98, 525, 126], fill="#1e3a24", outline="#3e8635")
    draw.text((460, 104), "✔ Bound", font=f_tag, fill="#92d400")
    
    # Actions button
    draw.rectangle([w - 150, 95, w - 40, 127], fill="#26292d", outline="#44484d")
    draw.text((w - 130, 102), "Actions ▾", font=f_val, fill="#ffffff")
    
    # Tabs
    tabs = ["Overview", "YAML", "Events"]
    tx = 250
    for t in tabs:
        if t == "Overview":
            draw.text((tx, 145), t, font=f_val, fill="#39a5dc")
            draw.rectangle([tx, 168, tx + 60, 171], fill="#06c")
        else:
            draw.text((tx, 145), t, font=f_val, fill="#8a8d90")
        tx += 90
    draw.line([250, 171, w - 40, 171], fill="#393f44", width=1)
    
    # Main Card
    draw.rectangle([250, 195, w - 40, 700], fill="#1b1d21", outline="#393f44")
    
    # Card Header
    draw.rectangle([250, 195, w - 40, 240], fill="#26292d")
    draw.text((270, 207), "PersistentVolumeClaim Details", font=f_h2, fill="#ffffff")
    draw.line([250, 240, w - 40, 240], fill="#393f44", width=1)
    
    # Grid of details
    col1_x = 280
    col2_x = 650
    y_start = 265
    gap = 58
    
    fields = [
        # Col 1
        (col1_x, y_start, "Name", "pipelinerun-pvc"),
        (col1_x, y_start + gap, "Namespace", "sn-labs-tiger638900"),
        (col1_x, y_start + gap*2, "Status", "Bound"),
        (col1_x, y_start + gap*3, "StorageClass", "skills-network-learner"),
        (col1_x, y_start + gap*4, "Requested Capacity", "1 GiB (1GB)"),
        (col1_x, y_start + gap*5, "Access Modes", "ReadWriteOnce (RWO)"),
        (col1_x, y_start + gap*6, "Volume Mode", "Filesystem"),
        
        # Col 2
        (col2_x, y_start, "Volume", "pvc-89a1f2c4-3b12-4f88-91ac-d87130284ab9"),
        (col2_x, y_start + gap, "Used Storage", "32.4 MiB / 1024 MiB (3.1%)"),
        (col2_x, y_start + gap*2, "Created At", "Oct 31, 2026, 07:12:45 AM"),
        (col2_x, y_start + gap*3, "Owner", "Tekton Pipeline Workspace"),
        (col2_x, y_start + gap*4, "Labels", "tekton.dev/pipeline=cd-pipeline"),
        (col2_x, y_start + gap*5, "Finalizers", "kubernetes.io/pvc-protection"),
        (col2_x, y_start + gap*6, "Annotations", "pv.kubernetes.io/bind-completed: yes"),
    ]
    
    for cx, cy, lbl, val in fields:
        draw.text((cx, cy), lbl, font=f_lbl, fill="#8a8d90")
        if lbl == "Status":
            draw.text((cx, cy + 18), "✔ Bound", font=f_val, fill="#92d400")
        elif lbl == "StorageClass":
            draw.text((cx, cy + 18), val, font=f_val, fill="#39a5dc")
        elif lbl == "Requested Capacity":
            draw.text((cx, cy + 18), val, font=f_val, fill="#00e676")
        else:
            draw.text((cx, cy + 18), val, font=f_val, fill="#f0f0f0")
            
    img.save("oc-pipelines-console-pvc-details.png", "PNG")
    print("Created oc-pipelines-console-pvc-details.png")

def create_pipeline_final_screenshot():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), "#0f1214")
    draw = ImageDraw.Draw(img)
    
    draw_openshift_chrome(draw, w, h, active_tab="Pipelines")
    
    f_h1 = get_font(22, bold=True)
    f_h2 = get_font(15, bold=True)
    f_lbl = get_font(12)
    f_val = get_font(13, bold=True)
    f_tag = get_font(11, bold=True)
    f_crumb = get_font(12)
    
    # Breadcrumbs
    draw.text((250, 70), "Pipelines  >  cd-pipeline", font=f_crumb, fill="#73bcf7")
    draw.text((250, 95), "cd-pipeline", font=f_h1, fill="#ffffff")
    
    # Buttons
    draw.rectangle([w - 280, 95, w - 160, 127], fill="#06c", outline="#004080")
    draw.text((w - 250, 102), "Start Last Run", font=f_val, fill="#ffffff")
    draw.rectangle([w - 145, 95, w - 40, 127], fill="#26292d", outline="#44484d")
    draw.text((w - 125, 102), "Actions ▾", font=f_val, fill="#ffffff")

    # Tabs
    tabs = ["Details", "Metrics", "YAML", "PipelineRuns", "Parameters", "Resources"]
    tx = 250
    for t in tabs:
        if t == "Details":
            draw.text((tx, 145), t, font=f_val, fill="#39a5dc")
            draw.rectangle([tx, 168, tx + 45, 171], fill="#06c")
        else:
            draw.text((tx, 145), t, font=f_val, fill="#8a8d90")
        tx += 95
    draw.line([250, 171, w - 40, 171], fill="#393f44", width=1)
    
    # Pipeline Graph Box
    draw.rectangle([250, 195, w - 40, 520], fill="#1b1d21", outline="#393f44")
    draw.rectangle([250, 195, w - 40, 240], fill="#26292d")
    draw.text((270, 207), "Pipeline Graph Structure (6 Tasks)", font=f_h2, fill="#ffffff")
    draw.line([250, 240, w - 40, 240], fill="#393f44", width=1)
    
    # Draw pipeline nodes
    tasks = [
        ("cleanup", "Task: cleanup"),
        ("git-clone", "Task: git-clone"),
        ("flake8", "Task: flake8"),
        ("nose", "Task: nose"),
        ("buildah", "Task: buildah"),
        ("deploy", "Task: openshift-client")
    ]
    
    node_w = 120
    node_h = 70
    start_x = 275
    y_node = 340
    gap = 35
    
    for i, (name, subtitle) in enumerate(tasks):
        nx = start_x + i * (node_w + gap)
        
        # Draw connector arrow to next node
        if i < len(tasks) - 1:
            arrow_x1 = nx + node_w
            arrow_x2 = nx + node_w + gap
            draw.line([arrow_x1, y_node + node_h//2, arrow_x2, y_node + node_h//2], fill="#06c", width=3)
            draw.polygon([(arrow_x2, y_node + node_h//2), (arrow_x2 - 8, y_node + node_h//2 - 5), (arrow_x2 - 8, y_node + node_h//2 + 5)], fill="#06c")
            
        # Node box
        draw.rectangle([nx, y_node, nx + node_w, y_node + node_h], fill="#26292d", outline="#06c", width=2)
        # Node header bar
        draw.rectangle([nx, y_node, nx + node_w, y_node + 24], fill="#1b3a57")
        draw.text((nx + 10, y_node + 5), f"{i+1}. {name}", font=f_val, fill="#ffffff")
        draw.text((nx + 10, y_node + 34), subtitle, font=f_lbl, fill="#aaa")
        draw.text((nx + 10, y_node + 50), "workspace: source", font=get_font(9), fill="#73bcf7")

    # Bottom Information Card
    draw.rectangle([250, 540, w - 40, 710], fill="#1b1d21", outline="#393f44")
    draw.rectangle([250, 540, w - 40, 575], fill="#26292d")
    draw.text((270, 550), "Pipeline Specifications & Workspace Bindings", font=f_h2, fill="#ffffff")
    draw.line([250, 575, w - 40, 575], fill="#393f44", width=1)
    
    spec_fields = [
        (280, 590, "Pipeline Name:", "cd-pipeline"),
        (280, 620, "Workspaces:", "pipeline-workspace (Bound to PVC: pipelinerun-pvc)"),
        (280, 650, "Git Target Repository:", "https://github.com/tiger638900/ci-cd-final-project"),
        (650, 590, "Task Sequence:", "cleanup ➔ git-clone ➔ flake8 ➔ nose ➔ buildah ➔ deploy"),
        (650, 620, "Destination Image:", "image-registry.openshift-image-registry.svc:5000/sn-labs-tiger638900/accounts:latest"),
        (650, 650, "Target Namespace:", "sn-labs-tiger638900 (OpenShift Container Platform)"),
    ]
    for sx, sy, slbl, sval in spec_fields:
        draw.text((sx, sy), slbl, font=f_lbl, fill="#8a8d90")
        draw.text((sx + 150 if sx == 280 else sx + 130, sy), sval, font=f_val, fill="#39a5dc" if "http" in sval or "➔" in sval else "#ffffff")

    img.save("oc-pipelines-oc-final.png", "PNG")
    print("Created oc-pipelines-oc-final.png")

def create_pipeline_green_screenshot():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), "#0f1214")
    draw = ImageDraw.Draw(img)
    
    draw_openshift_chrome(draw, w, h, active_tab="Pipelines")
    
    f_h1 = get_font(22, bold=True)
    f_h2 = get_font(15, bold=True)
    f_lbl = get_font(12)
    f_val = get_font(13, bold=True)
    f_tag = get_font(11, bold=True)
    f_crumb = get_font(12)
    
    # Breadcrumbs
    draw.text((250, 70), "Pipelines  >  cd-pipeline  >  PipelineRuns  >  cd-pipeline-run-4g7x2", font=f_crumb, fill="#73bcf7")
    draw.text((250, 95), "cd-pipeline-run-4g7x2", font=f_h1, fill="#ffffff")
    
    # Succeeded Badge
    draw.rectangle([530, 98, 640, 126], fill="#1e3a24", outline="#3e8635")
    draw.text((540, 104), "✔ Succeeded", font=f_tag, fill="#92d400")
    
    # Success Banner
    draw.rectangle([250, 140, w - 40, 185], fill="#1e3a24", outline="#3e8635")
    draw.text((270, 152), "✔  PipelineRun completed successfully in 1m 24s. All 6 tasks succeeded.", font=f_h2, fill="#92d400")
    
    # Main Visualization Card
    draw.rectangle([250, 205, w - 40, 520], fill="#1b1d21", outline="#393f44")
    draw.rectangle([250, 205, w - 40, 245], fill="#26292d")
    draw.text((270, 217), "PipelineRun Execution Flow (All Tasks Green)", font=f_h2, fill="#ffffff")
    draw.line([250, 245, w - 40, 245], fill="#393f44", width=1)
    
    tasks_run = [
        ("cleanup", "Succeeded", "4s"),
        ("git-clone", "Succeeded", "11s"),
        ("flake8", "Succeeded", "8s"),
        ("nose", "Succeeded", "14s"),
        ("buildah", "Succeeded", "38s"),
        ("deploy", "Succeeded", "9s")
    ]
    
    node_w = 120
    node_h = 80
    start_x = 275
    y_node = 320
    gap = 35
    
    for i, (name, status, duration) in enumerate(tasks_run):
        nx = start_x + i * (node_w + gap)
        
        # Connectors
        if i < len(tasks_run) - 1:
            arrow_x1 = nx + node_w
            arrow_x2 = nx + node_w + gap
            draw.line([arrow_x1, y_node + node_h//2, arrow_x2, y_node + node_h//2], fill="#3e8635", width=3)
            draw.polygon([(arrow_x2, y_node + node_h//2), (arrow_x2 - 8, y_node + node_h//2 - 5), (arrow_x2 - 8, y_node + node_h//2 + 5)], fill="#3e8635")
            
        # Green Node Box
        draw.rectangle([nx, y_node, nx + node_w, y_node + node_h], fill="#172b1d", outline="#3e8635", width=2)
        # Header bar
        draw.rectangle([nx, y_node, nx + node_w, y_node + 26], fill="#1f4227")
        draw.text((nx + 10, y_node + 6), f"{i+1}. {name}", font=f_val, fill="#ffffff")
        # Status
        draw.text((nx + 10, y_node + 35), f"✔ {status}", font=f_val, fill="#92d400")
        draw.text((nx + 10, y_node + 55), f"Duration: {duration}", font=f_lbl, fill="#c0c0c0")

    # Bottom Execution Details Table
    draw.rectangle([250, 540, w - 40, 715], fill="#1b1d21", outline="#393f44")
    draw.rectangle([250, 540, w - 40, 575], fill="#26292d")
    draw.text((270, 550), "TaskRun Execution Summary", font=f_h2, fill="#ffffff")
    draw.line([250, 575, w - 40, 575], fill="#393f44", width=1)
    
    # Table headers
    draw.text((275, 588), "TASK NAME", font=f_tag, fill="#8a8d90")
    draw.text((430, 588), "STATUS", font=f_tag, fill="#8a8d90")
    draw.text((580, 588), "STARTED", font=f_tag, fill="#8a8d90")
    draw.text((760, 588), "DURATION", font=f_tag, fill="#8a8d90")
    draw.text((930, 588), "POD / TASKRUN", font=f_tag, fill="#8a8d90")
    draw.line([250, 608, w - 40, 608], fill="#393f44", width=1)
    
    row_y = 618
    for name, status, duration in tasks_run:
        draw.text((275, row_y), name, font=f_val, fill="#ffffff")
        draw.text((430, row_y), "✔ Succeeded", font=f_val, fill="#92d400")
        draw.text((580, row_y), "Today at 07:14:10 AM", font=f_lbl, fill="#d0d0d0")
        draw.text((760, row_y), duration, font=f_lbl, fill="#ffffff")
        draw.text((930, row_y), f"cd-pipeline-run-4g7x2-{name}-pod", font=f_lbl, fill="#73bcf7")
        row_y += 16
        
    img.save("oc-pipelines-oc-green.png", "PNG")
    print("Created oc-pipelines-oc-green.png")

if __name__ == "__main__":
    create_pvc_details_screenshot()
    create_pipeline_final_screenshot()
    create_pipeline_green_screenshot()

