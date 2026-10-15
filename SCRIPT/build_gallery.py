# -*- coding: utf-8 -*-
"""
build_gallery.py
自动化扫描 Blockbench 3D 模型与 TTS 角色语音，构建精美的单页 3D 展示平台 (index.html)
安全红线：不修改、添加或删除 Blockbench 和 TTS 文件夹内的任何文件。
输出目标：根目录下的 index.html
"""

import os
import re
import json

def get_character_display_meta(name):
    meta = {
        'BakaBot8266': {
            'title': 'Baka_Bot_9000 (故障美食家·铁皮人)',
            'tag': '极度熟度要求 · 工业零件论',
            'desc': '复古 CRT 显示器脑袋，屏幕显示 (ᗜ ˰ ᗜ) 颜文字。把烤肉当成工业零件和能源电池包，需要极端的熟度（全熟或烧焦），否则会判定系统过载启动自爆！',
            'avatar': '🤖'
        },
        'Chef': {
            'title': 'Chef (烤肉大厨)',
            'tag': '烤肉原神 · 炭火掌控者',
            'desc': '阿根廷传统 Parrilla 首席烤肉大师，身手娴熟，掌握火候与食材的极致平衡。',
            'avatar': '👨‍🍳'
        },
        'DonMateo': {
            'title': 'Don_Mateo (暴躁老叔)',
            'tag': '传统烤肉原教旨主义者',
            'desc': '地中海花白头发，浓密八字胡。对火候极其严苛，坚信正宗阿根廷烤肉必须多汁外焦里嫩，差一秒就会当场掀桌！',
            'avatar': '👴'
        },
        'ElCarbonero': {
            'title': 'El Carbonero (噬炭怪人·阿炭)',
            'tag': '专吃纯黑焦炭 (Burnt)',
            'desc': '黑灰焦炭爆炸头，嘴角满是黑煤灰。拒绝正常多汁肉类，指名道姓要烤到彻底焦黑（Burnt）嘎嘣脆、甚至想直接生啃炉膛里烧红的木炭！',
            'avatar': '🔥'
        },
        'Momo': {
            'title': 'Momo (大胃王呆毛吃货娘)',
            'tag': '急不可耐 · 快熟主义',
            'desc': '蜜桃粉短发带呆毛，星星眼流口水。嘴急等不及，偏爱快熟的三分熟（Rare）或五分熟（Medium），幸福感拉满的大吃货！',
            'avatar': '🍑'
        },
        'Rikka': {
            'title': 'Rikka (中二病眼罩少女)',
            'tag': '暗黑魔血 · 偏爱见血生肉',
            'desc': '深紫双马尾，右眼医用眼罩。自称右眼渴求淌着暗黑魔血的排骨与凝血魔肠，偏爱 Rare（三分熟）与 Medium（五分熟）！',
            'avatar': '👁️'
        },
        'SakuraGyaruo': {
            'title': 'Sakura_Gyaruo (挑剔辣妹)',
            'tag': '拍照出片 · 杜绝寄生虫',
            'desc': '金粉渐变大波浪卷发，JK 开衫配泡泡袜。怕寄生虫又怕黑边，只吃 Well Done（全熟）或爆汁 Medium（五分熟），拍美美照片发社交平台！',
            'avatar': '💅'
        },
        'UgaChan': {
            'title': 'Uga_Chan (远古野人少女·乌嘎酱)',
            'tag': '火是坏文明 · 只吃纯生肉 (Raw)',
            'desc': '狂野棕红长发插着兽骨发饰，身穿豹纹兽皮短裙。拒绝火文明，直接生啃全生（Raw）排骨与生鸡肉，见血就吃的部落小野人！',
            'avatar': '🍖'
        },
        'Yuki': {
            'title': 'Yuki (三无沉默可爱少女)',
            'tag': '温柔口感 · 默默盯视',
            'desc': '银白姬发式长直发，大围巾遮住下巴。说话轻声细语，偏爱恰到好处的温柔口感（Medium / Well Done），不满意时会发出幽幽叹息。',
            'avatar': '🧣'
        }
    }
    return meta.get(name, {
        'title': name,
        'tag': '游戏角色',
        'desc': '游戏中的顾客角色模型。',
        'avatar': '👤'
    })

def get_food_display_meta(name):
    meta = {
        'Chorizo': {
            'title': 'Chorizo (阿根廷烤香肠)',
            'tag': '前菜垫胃 · 鲜美爆汁',
            'desc': '阿根廷 Parrilla 经典开胃香肠，表皮滋滋冒油，内里香料与猪肉香气四溢。五分熟弹嫩多汁，全熟焦香诱人。',
            'icon': '🌭'
        },
        'Costilla': {
            'title': 'Costilla (阿根廷横切牛排骨)',
            'tag': '镇店之宝 · Asado 灵魂',
            'desc': '传统阿根廷烤排骨（Asado de Tira），骨边肉香浓郁，脂肪经木炭慢烤融化，三分熟见血多汁，全熟骨肉分离。',
            'icon': '🥩'
        },
        'Matambre': {
            'title': 'Matambre (牛腹肉 / 夹心肉排)',
            'tag': '薄嫩焦脆 · 肉汁饱满',
            'desc': '牛腹部特有的珍稀薄肉层，既可烤到全熟如黄油般软嫩，也可快速翻面做成三分熟极品。',
            'icon': '🥓'
        },
        'Morcilla': {
            'title': 'Morcilla (阿根廷黑血肠)',
            'tag': '软糯浓郁 · 碳化能量',
            'desc': '黑油电池包般的经典血肠，外脆内糯，富含铁质与香料风味，是机器人与吃货娘的大爱。',
            'icon': '🥘'
        },
        'Pollo': {
            'title': 'Pollo (秘制香烤鸡肉)',
            'tag': '金黄脆皮 · 低脂饱腹',
            'desc': '新鲜鸡肉经炭火洗礼，外皮金黄酥脆，肉质鲜嫩弹牙。是挑剔辣妹与呆毛吃货娘的心头好。',
            'icon': '🍗'
        }
    }
    return meta.get(name, {
        'title': name,
        'tag': '烧烤食材',
        'desc': 'Parrilla 烧烤食材模型。',
        'icon': '🍽️'
    })

def get_building_display_meta(name):
    meta = {
        'Brasero': {
            'title': 'Brasero (引炭引火铁笼)',
            'tag': '炭火核心 · 生火源泉',
            'desc': '传统阿根廷烤肉架侧边的引火铁笼，木柴在此充分燃烧化为滚烫通红的木炭块，再用炭铲拨入烤架下方。',
            'icon': '🏮'
        },
        'CharCoalPytamid': {
            'title': 'CharCoal Pyramid (金字塔型木炭堆)',
            'tag': '燃料储备 · 纯正焦香',
            'desc': '整齐码放的纯天然硬木炭堆，为持续一整天的 Asado 盛宴提供持久而纯净的高温火力。',
            'icon': '⛰️'
        },
        'Mesa': {
            'title': 'Mesa de Madera (原木料理长桌)',
            'tag': '案板台面 · 备餐盛宴',
            'desc': '厚重粗犷的实木料理操作台，用于切割牛排、撒粗盐与装盘大块肉品。',
            'icon': '🪵'
        },
        'Parrilla': {
            'title': 'La Parrilla (阿根廷传统烤架)',
            'tag': '核心设施 · V型排油槽',
            'desc': '经典带滑轮升降装置与斜向 V 型导油槽的烤肉架，能够精准控制肉排与炭火的距离，避免油脂滴入起明火。',
            'icon': '🏭'
        },
        '烧红的木炭': {
            'title': '烧红的木炭 (Glowing Charcoal)',
            'tag': '炽热纯炭 · 噬炭怪人至爱',
            'desc': '炉底烧到通体赤红、热浪滚滚的极品木炭，发出滋滋微光，温度高达数百摄氏度。',
            'icon': '🔥'
        }
    }
    return meta.get(name, {
        'title': name,
        'tag': '场景建筑',
        'desc': '阿根廷烤肉店场景建筑与设备模型。',
        'icon': '🏠'
    })

def scan_gallery_data(root_dir):
    blockbench_dir = os.path.join(root_dir, 'Blockbench')
    tts_dir = os.path.join(root_dir, 'TTS')
    
    categories = {
        'characters': {
            'path': os.path.join(blockbench_dir, 'Characters'),
            'label': '角色 (Characters)',
            'icon': '👤'
        },
        'food': {
            'path': os.path.join(blockbench_dir, 'Food'),
            'label': '食物 (Food)',
            'icon': '🍖'
        },
        'buildings': {
            'path': os.path.join(blockbench_dir, '建筑'),
            'label': '建筑 (Buildings)',
            'icon': '🏠'
        }
    }
    
    # 1. 扫描 Blockbench 模型
    models = []
    for cat_key, cat_info in categories.items():
        cat_path = cat_info['path']
        if not os.path.exists(cat_path):
            continue
            
        for folder_name in sorted(os.listdir(cat_path)):
            sub_path = os.path.join(cat_path, folder_name)
            if not os.path.isdir(sub_path):
                continue
                
            files = os.listdir(sub_path)
            
            # 模型优先级：.glb > .gltf > .bbmodel > .fbx
            model_file = None
            for ext in ['.glb', '.gltf', '.bbmodel', '.fbx']:
                cands = [f for f in files if f.lower().endswith(ext)]
                if cands:
                    preferred = [f for f in cands if folder_name.lower() in f.lower()]
                    model_file = preferred[0] if preferred else cands[0]
                    break
                    
            texture_file = None
            pngs = [f for f in files if f.lower().endswith('.png') and not f.lower().endswith('_preview.png')]
            if pngs:
                texture_file = pngs[0]
                
            preview_file = None
            previews = [f for f in files if 'preview' in f.lower() and f.lower().endswith('.png')]
            if previews:
                preview_file = previews[0]
            elif texture_file:
                preview_file = texture_file
                
            rel_model = os.path.relpath(os.path.join(sub_path, model_file), root_dir).replace('\\', '/') if model_file else None
            rel_texture = os.path.relpath(os.path.join(sub_path, texture_file), root_dir).replace('\\', '/') if texture_file else None
            rel_preview = os.path.relpath(os.path.join(sub_path, preview_file), root_dir).replace('\\', '/') if preview_file else None
            
            # 元数据补充
            if cat_key == 'characters':
                disp = get_character_display_meta(folder_name)
            elif cat_key == 'food':
                disp = get_food_display_meta(folder_name)
            else:
                disp = get_building_display_meta(folder_name)
                
            model_item = {
                'id': f"{cat_key}_{folder_name.lower()}",
                'name': folder_name,
                'title': disp.get('title', folder_name),
                'tag': disp.get('tag', ''),
                'desc': disp.get('desc', ''),
                'icon': disp.get('icon', disp.get('avatar', '📦')),
                'category': cat_key,
                'folder_name': folder_name,
                'model_file': rel_model,
                'model_type': model_file.split('.')[-1].lower() if model_file else 'none',
                'texture_file': rel_texture,
                'preview_file': rel_preview,
                'all_files': files,
                'tts_key': None
            }
            models.append(model_item)
            
    # 2. 扫描 TTS 语音
    tts_data = {}
    if os.path.exists(tts_dir):
        for char_folder in sorted(os.listdir(tts_dir)):
            char_path = os.path.join(tts_dir, char_folder)
            if not os.path.isdir(char_path):
                continue
                
            m_short = re.match(r'^([a-zA-Z0-9_]+)', char_folder)
            short_name = m_short.group(1) if m_short else char_folder.split(' ')[0]
            
            actions = {}
            for action_name in sorted(os.listdir(char_path)):
                action_path = os.path.join(char_path, action_name)
                if not os.path.isdir(action_path):
                    continue
                    
                languages = {}
                action_condition = ""
                action_food = ""
                action_doneness = ""
                
                for lang in ['CN', 'ES', 'US']:
                    lang_path = os.path.join(action_path, lang)
                    if not os.path.exists(lang_path):
                        continue
                        
                    wavs = [f for f in os.listdir(lang_path) if f.lower().endswith('.wav')]
                    wav_file = os.path.relpath(os.path.join(lang_path, wavs[0]), root_dir).replace('\\', '/') if wavs else None
                    
                    sub_file = os.path.join(lang_path, 'subtitle.txt')
                    game_sub = ""
                    tts_text = ""
                    if os.path.exists(sub_file):
                        try:
                            with open(sub_file, 'r', encoding='utf-8') as sf:
                                sub_content = sf.read()
                                m_sub = re.search(r'\[游戏字幕\]\s*\n(.*?)(?=\n\n|\n\[|\Z)', sub_content, re.DOTALL)
                                if m_sub:
                                    game_sub = m_sub.group(1).strip()
                                m_tts = re.search(r'\[TTS合成文本\]\s*\n(.*?)(?=\n\n|\n\[|\Z)', sub_content, re.DOTALL)
                                if m_tts:
                                    tts_text = m_tts.group(1).strip()
                        except:
                            pass
                            
                    info_file = os.path.join(lang_path, 'info.json')
                    info_data = {}
                    if os.path.exists(info_file):
                        try:
                            with open(info_file, 'r', encoding='utf-8') as jf:
                                info_data = json.load(jf)
                                action_condition = info_data.get('condition', action_condition)
                                action_food = info_data.get('food', action_food)
                                action_doneness = info_data.get('doneness', action_doneness)
                        except:
                            pass
                            
                    languages[lang] = {
                        'wav': wav_file,
                        'subtitle': game_sub,
                        'tts_text': tts_text,
                        'voice': info_data.get('voice', ''),
                        'speed': info_data.get('speed', 0.8),
                        'pitch': info_data.get('pitch', 0.0),
                        'timbre_mode': info_data.get('timbre_mode', '')
                    }
                    
                actions[action_name] = {
                    'condition': action_condition,
                    'food': action_food,
                    'doneness': action_doneness,
                    'languages': languages
                }
                
            tts_data[char_folder] = {
                'short_name': short_name,
                'full_folder': char_folder,
                'actions': actions
            }
            
    # 3. 关联角色模型与 TTS 语音
    for m in models:
        if m['category'] == 'characters':
            m_clean = re.sub(r'[^a-z0-9]', '', m['name'].lower())
            for t_key, t_val in tts_data.items():
                t_clean = re.sub(r'[^a-z0-9]', '', t_val['short_name'].lower())
                if m_clean in t_clean or t_clean in m_clean or m_clean.startswith(t_clean[:6]) or t_clean.startswith(m_clean[:6]):
                    m['tts_key'] = t_key
                    break
                    
    return {
        'models': models,
        'tts': tts_data
    }

def generate_html_content(data):
    json_data_str = json.dumps(data, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Argentine Asado 3D Gallery & Kokoro TTS Studio</title>
  
  <!-- Google model-viewer 官方库 -->
  <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
  
  <!-- Three.js 及 FBX/OrbitControls 支持 (用于渲染 .bbmodel 与 .fbx) -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/fflate@0.8.0/umd/index.js"></script>
  <!-- 引入热修复后的 Blockbench ASCII FBXLoader (彻底解决 Unknown format 与 undefined.name 错误) -->
  <script src="SCRIPT/three_fbx_loader.js"></script>
  <script>
    if (typeof THREE.FBXLoader === 'undefined') {{
      fetch('https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/FBXLoader.js')
        .then(r => r.text())
        .then(code => {{
          code = code.replace('function isFbxFormatASCII( text ) {{', 'function isFbxFormatASCII( text ) {{ return true;');
          code = code.replace('const parentName = currentNode.name;', 'if (!currentNode) return; const parentName = currentNode.name;');
          const s = document.createElement('script');
          s.textContent = code;
          document.head.appendChild(s);
        }}).catch(e => console.error("CDN FBXLoader fallback failed:", e));
    }}
  </script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

  <style>
    :root {{
      --bg-dark: #0a0e17;
      --bg-panel: rgba(18, 24, 38, 0.85);
      --bg-card: rgba(28, 36, 56, 0.65);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-glow: rgba(56, 189, 248, 0.3);
      --primary: #38bdf8;
      --primary-glow: 0 0 20px rgba(56, 189, 248, 0.4);
      --accent-orange: #fb923c;
      --accent-green: #34d399;
      --accent-pink: #f472b6;
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --radius: 16px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}

    body {{
      background: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.07) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(251, 146, 60, 0.07) 0%, transparent 40%),
        linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
      display: flex;
      flex-direction: column;
    }}

    /* 顶部导航与 Header */
    header {{
      padding: 20px 32px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-color);
      backdrop-filter: blur(20px);
      background: rgba(10, 14, 23, 0.7);
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .logo-group {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .logo-icon {{
      font-size: 32px;
      background: linear-gradient(135deg, #fb923c, #ef4444);
      width: 48px;
      height: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 12px;
      box-shadow: 0 4px 15px rgba(239, 68, 68, 0.35);
    }}

    .logo-text h1 {{
      font-size: 20px;
      font-weight: 700;
      letter-spacing: -0.5px;
      background: linear-gradient(90deg, #ffffff, #94a3b8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .logo-text p {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* 主分类 Tabs */
    .tabs-nav {{
      display: flex;
      gap: 8px;
      background: rgba(255, 255, 255, 0.04);
      padding: 6px;
      border-radius: 14px;
      border: 1px solid var(--border-color);
    }}

    .tab-btn {{
      background: transparent;
      border: none;
      outline: none;
      padding: 10px 22px;
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      border-radius: 10px;
      transition: all 0.25s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .tab-btn:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
    }}

    .tab-btn.active {{
      background: var(--primary);
      color: #0b0f19;
      box-shadow: var(--primary-glow);
    }}

    .tab-btn.tab-food.active {{
      background: var(--accent-orange);
      box-shadow: 0 0 20px rgba(251, 146, 60, 0.4);
    }}

    .tab-btn.tab-buildings.active {{
      background: var(--accent-green);
      box-shadow: 0 0 20px rgba(52, 211, 153, 0.4);
    }}

    .header-stats {{
      display: flex;
      gap: 16px;
    }}

    .stat-pill {{
      padding: 6px 14px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      font-size: 12px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .stat-pill b {{
      color: var(--primary);
    }}

    /* 主布局 */
    main {{
      flex: 1;
      display: grid;
      grid-template-columns: 320px 1fr 420px;
      gap: 20px;
      padding: 20px 24px;
      height: calc(100vh - 85px);
    }}

    /* 左侧模型列表 */
    .panel-list {{
      background: var(--bg-panel);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .panel-header {{
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .panel-header h2 {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .search-box {{
      padding: 12px 18px;
      border-bottom: 1px solid var(--border-color);
    }}

    .search-box input {{
      width: 100%;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 9px 14px;
      font-size: 13px;
      color: #fff;
      outline: none;
      transition: all 0.2s;
    }}

    .search-box input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }}

    .item-scroll-list {{
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .item-scroll-list::-webkit-scrollbar {{
      width: 6px;
    }}
    .item-scroll-list::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.15);
      border-radius: 3px;
    }}

    .model-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 12px 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: all 0.2s ease;
      position: relative;
      overflow: hidden;
    }}

    .model-card:hover {{
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-1px);
    }}

    .model-card.active {{
      border-color: var(--primary);
      background: rgba(56, 189, 248, 0.12);
      box-shadow: inset 0 0 15px rgba(56, 189, 248, 0.15);
    }}

    .model-card.active::before {{
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: var(--primary);
    }}

    .card-icon-wrap {{
      width: 44px;
      height: 44px;
      border-radius: 10px;
      background: rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      border: 1px solid var(--border-color);
      flex-shrink: 0;
      position: relative;
    }}

    .card-icon-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 8px;
      image-rendering: pixelated;
    }}

    .card-info {{
      flex: 1;
      min-width: 0;
    }}

    .card-title {{
      font-size: 13.5px;
      font-weight: 600;
      color: #fff;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .card-sub {{
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 3px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .card-badge {{
      font-size: 10px;
      padding: 3px 7px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}

    /* 中间 3D 渲染舞台 */
    .panel-stage {{
      background: var(--bg-panel);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }}

    .stage-topbar {{
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-color);
      background: rgba(0, 0, 0, 0.2);
      z-index: 10;
    }}

    .stage-title-wrap h3 {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .stage-title-wrap p {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 3px;
    }}

    .stage-controls {{
      display: flex;
      gap: 8px;
    }}

    .tool-btn {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .tool-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }}

    .tool-btn.active {{
      background: var(--primary);
      color: #0b0f19;
      font-weight: 600;
    }}

    .viewport-container {{
      flex: 1;
      position: relative;
      background: radial-gradient(circle at center, #162035 0%, #0d121f 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}

    /* model-viewer 标签样式 */
    model-viewer {{
      width: 100%;
      height: 100%;
      outline: none;
      --poster-color: transparent;
      display: none;
    }}

    /* Three.js Canvas 样式 */
    #three-canvas {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    /* 3D 加载提示 */
    .loader-overlay {{
      position: absolute;
      inset: 0;
      background: rgba(10, 14, 23, 0.7);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      z-index: 5;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.3s;
    }}

    .loader-overlay.show {{
      opacity: 1;
    }}

    .spinner {{
      width: 38px;
      height: 38px;
      border: 3px solid rgba(56, 189, 248, 0.2);
      border-top-color: var(--primary);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }}

    @keyframes spin {{
      to {{ transform: rotate(360deg); }}
    }}

    .stage-format-badge {{
      position: absolute;
      bottom: 16px;
      left: 16px;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(8px);
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 11px;
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 8px;
      z-index: 10;
    }}

    .dot-live {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--accent-green);
      box-shadow: 0 0 8px var(--accent-green);
    }}

    /* 右侧控制台面板 (TTS 语音与材质详情) */
    .panel-console {{
      background: var(--bg-panel);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .tts-scroll-area {{
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .tts-scroll-area::-webkit-scrollbar {{
      width: 6px;
    }}
    .tts-scroll-area::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.15);
      border-radius: 3px;
    }}

    /* 角色资料卡 */
    .character-profile-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .profile-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .profile-name {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
    }}

    .profile-tag {{
      font-size: 11px;
      color: var(--accent-orange);
      background: rgba(251, 146, 60, 0.12);
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 600;
    }}

    .profile-desc {{
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    /* 动作与语音场景卡片 */
    .action-group-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      overflow: hidden;
      transition: border-color 0.2s;
    }}

    .action-group-card:hover {{
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .action-header {{
      padding: 10px 14px;
      background: rgba(0, 0, 0, 0.25);
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-color);
    }}

    .action-title {{
      font-size: 13px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .action-cond {{
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 4px;
      background: rgba(56, 189, 248, 0.12);
      color: var(--primary);
      font-weight: 600;
    }}

    .lang-btn-grid {{
      padding: 12px 14px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }}

    .voice-btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 9px 8px;
      color: #fff;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }}

    .voice-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-1px);
    }}

    .voice-btn.playing {{
      border-color: var(--accent-green);
      background: rgba(52, 211, 153, 0.18);
      box-shadow: 0 0 14px rgba(52, 211, 153, 0.3);
    }}

    .voice-btn .lang-flag {{
      font-size: 16px;
    }}

    .voice-btn .lang-label {{
      font-size: 11px;
    }}

    /* 正在播放的字幕横幅卡片 */
    .now-playing-card {{
      background: rgba(15, 23, 42, 0.95);
      border-top: 1px solid var(--border-color);
      padding: 14px 18px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      border-left: 4px solid var(--accent-green);
    }}

    .playing-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .playing-tag {{
      font-size: 11px;
      color: var(--accent-green);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .playing-subtitle {{
      font-size: 13.5px;
      color: #fff;
      line-height: 1.5;
      font-weight: 500;
    }}

    .playing-tts {{
      font-size: 12px;
      color: var(--accent-orange);
      line-height: 1.4;
      font-style: italic;
    }}

    .playing-meta {{
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    /* 非角色详情面板 (食物 & 建筑) */
    .asset-detail-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .detail-row {{
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 12.5px;
    }}

    .detail-row:last-child {{
      border-bottom: none;
    }}

    .detail-label {{
      color: var(--text-muted);
    }}

    .detail-val {{
      color: #fff;
      font-weight: 600;
    }}

    .texture-preview-box {{
      margin-top: 8px;
      border: 1px dashed var(--border-color);
      border-radius: 10px;
      padding: 10px;
      text-align: center;
      background: rgba(0, 0, 0, 0.3);
    }}

    .texture-preview-box img {{
      max-width: 140px;
      max-height: 140px;
      border-radius: 6px;
      image-rendering: pixelated;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }}

    /* 响应式适配 */
    @media (max-width: 1200px) {{
      main {{
        grid-template-columns: 280px 1fr 340px;
      }}
    }}

    @media (max-width: 992px) {{
      body {{
        overflow-y: auto;
      }}
      main {{
        grid-template-columns: 1fr;
        height: auto;
      }}
      .panel-stage {{
        height: 480px;
      }}
    }}
  </style>
</head>
<body>

  <!-- 顶部 Header -->
  <header>
    <div class="logo-group">
      <div class="logo-icon">🥩</div>
      <div class="logo-text">
        <h1>Argentine Asado 3D Gallery & Studio</h1>
        <p>Blockbench 像素模型与 Kokoro 多语言 TTS 语音联动展示台</p>
      </div>
    </div>

    <!-- 三大主分类 Tab -->
    <nav class="tabs-nav">
      <button class="tab-btn active tab-characters" onclick="switchCategory('characters')">
        <span>👤</span> 角色 (Characters)
      </button>
      <button class="tab-btn tab-food" onclick="switchCategory('food')">
        <span>🍖</span> 食物 (Food)
      </button>
      <button class="tab-btn tab-buildings" onclick="switchCategory('buildings')">
        <span>🏠</span> 建筑 (Buildings)
      </button>
    </nav>

    <!-- 状态指示 -->
    <div class="header-stats">
      <div class="stat-pill">
        <span>模型总量:</span> <b id="stat-model-count">0</b>
      </div>
      <div class="stat-pill">
        <span>TTS 语音:</span> <b id="stat-voice-count">0 条 (3语)</b>
      </div>
    </div>
  </header>

  <!-- 主体工作区 -->
  <main>
    <!-- 左侧：模型资源列表 -->
    <section class="panel-list">
      <div class="panel-header">
        <h2 id="list-panel-title"><span>👤</span> 角色列表</h2>
        <span class="card-badge" id="list-count-badge">0 项</span>
      </div>
      <div class="search-box">
        <input type="text" id="model-search-input" placeholder="🔍 搜索模型名称或特性..." oninput="handleSearch(this.value)">
      </div>
      <div class="item-scroll-list" id="model-item-list">
        <!-- 动态注入列表卡片 -->
      </div>
    </section>

    <!-- 中间：3D 核心舞台 -->
    <section class="panel-stage">
      <div class="stage-topbar">
        <div class="stage-title-wrap">
          <h3 id="stage-model-title">请选择一个模型</h3>
          <p id="stage-model-desc">支持 360 度自由旋转、缩放与平移查看细节</p>
        </div>
        <div class="stage-controls">
          <button class="tool-btn active" id="btn-autorotate" onclick="toggleAutoRotate()">
            <span>🔄</span> 自动旋转
          </button>
          <button class="tool-btn" id="btn-wireframe" onclick="toggleWireframe()">
            <span>📐</span> 线框模式
          </button>
          <button class="tool-btn" onclick="resetCamera()">
            <span>🎯</span> 复位视角
          </button>
        </div>
      </div>

      <div class="viewport-container" id="viewport-box">
        <!-- Google model-viewer 官方查看器 (支持 .glb / .gltf) -->
        <model-viewer id="main-model-viewer"
          camera-controls
          auto-rotate
          rotation-per-second="20deg"
          shadow-intensity="1.2"
          shadow-softness="0.8"
          exposure="1.0"
          interaction-prompt="none"
          alt="Argentine Asado 3D Model">
        </model-viewer>

        <!-- Three.js Canvas (用于完美渲染 Blockbench .bbmodel 与 .fbx) -->
        <canvas id="three-canvas"></canvas>

        <!-- 加载动画 -->
        <div class="loader-overlay" id="stage-loader">
          <div class="spinner"></div>
          <div style="font-size: 13px; color: var(--primary);">正在渲染 3D 几何与纹理...</div>
        </div>

        <!-- 底部格式徽章 -->
        <div class="stage-format-badge">
          <div class="dot-live"></div>
          <span id="stage-format-text">WebGL 2.0 / PBR 渲染中</span>
        </div>
      </div>
    </section>

    <!-- 右侧：TTS 专属语音控制台 / 模型详情面板 -->
    <section class="panel-console">
      <div class="panel-header">
        <h2 id="console-panel-title"><span>🎙️</span> 角色专属语音控制台</h2>
        <span class="card-badge" id="console-mode-badge" style="color: var(--accent-green);">KOKORO 0.8x</span>
      </div>

      <div class="tts-scroll-area" id="console-scroll-content">
        <!-- 动态注入 TTS 控制项或资产详情卡片 -->
      </div>

      <!-- 实时台词与字幕横幅卡片 -->
      <div class="now-playing-card" id="now-playing-banner" style="display: none;">
        <div class="playing-header">
          <div class="playing-tag">
            <span class="dot-live"></span>
            <span id="playing-lang-tag">🇨🇳 正在播放</span>
          </div>
          <div class="card-badge" id="playing-voice-badge">zf_xiaoni · 0.8x</div>
        </div>
        <div class="playing-subtitle" id="playing-sub-text">“请稍候...”</div>
        <div class="playing-tts" id="playing-tts-text"></div>
        <div class="playing-meta" id="playing-meta-text">食材熟度判定：--</div>
      </div>
    </section>
  </main>

  <!-- 全局隐藏 HTML5 音频播放器 -->
  <audio id="tts-audio-player" preload="none"></audio>

  <!-- 注入 Python 扫描所得全部数据 -->
  <script>
    const GALLERY_DATA = {json_data_str};
  </script>

  <!-- 前端交互与 3D 渲染控制逻辑 -->
  <script>
    let currentCategory = 'characters';
    let currentModel = null;
    let autoRotate = true;
    let wireframeMode = false;
    let currentActiveVoiceBtn = null;

    // Three.js 全局对象
    let scene, camera, renderer, controls, currentMeshGroup = null;
    const canvas = document.getElementById('three-canvas');
    const modelViewer = document.getElementById('main-model-viewer');
    const audioPlayer = document.getElementById('tts-audio-player');

    // 初始化 Three.js 场景
    function initThreeScene() {{
      scene = new THREE.Scene();
      
      const rect = canvas.getBoundingClientRect();
      camera = new THREE.PerspectiveCamera(45, rect.width / rect.height, 0.1, 8000);
      camera.position.set(25, 20, 35);

      renderer = new THREE.WebGLRenderer({{ canvas: canvas, antialias: true, alpha: true }});
      renderer.setSize(rect.width, rect.height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;

      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.autoRotate = autoRotate;
      controls.autoRotateSpeed = 2.0;

      // 灯光设置
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
      scene.add(ambientLight);

      const dirLight = new THREE.DirectionalLight(0xfff5ea, 1.2);
      dirLight.position.set(30, 45, 25);
      dirLight.castShadow = true;
      scene.add(dirLight);

      const backLight = new THREE.DirectionalLight(0x38bdf8, 0.5);
      backLight.position.set(-25, 15, -25);
      scene.add(backLight);

      // 地面网格辅助
      const grid = new THREE.GridHelper(50, 25, 0x38bdf8, 0x1e293b);
      grid.position.y = -0.1;
      scene.add(grid);

      window.addEventListener('resize', onWindowResize);
      animate();
    }}

    function onWindowResize() {{
      const rect = canvas.parentElement.getBoundingClientRect();
      camera.aspect = rect.width / rect.height;
      camera.updateProjectionMatrix();
      renderer.setSize(rect.width, rect.height);
    }}

    function animate() {{
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }}

    // 解析 Blockbench .bbmodel 专属体素几何引擎
    async function loadBBModelFile(url, textureUrl) {{
      const loader = document.getElementById('stage-loader');
      loader.classList.add('show');
      
      try {{
        const response = await fetch(url);
        const data = await response.json();

        if (currentMeshGroup) {{
          scene.remove(currentMeshGroup);
        }}

        currentMeshGroup = new THREE.Group();
        const resWidth = (data.resolution && data.resolution.width) ? data.resolution.width : 64;
        const resHeight = (data.resolution && data.resolution.height) ? data.resolution.height : 64;

        // 纹理加载（支持 embedded base64 或外部 png）
        let texture;
        if (data.textures && data.textures.length > 0 && data.textures[0].source && data.textures[0].source.startsWith('data:')) {{
          texture = new THREE.TextureLoader().load(data.textures[0].source);
        }} else if (textureUrl) {{
          texture = new THREE.TextureLoader().load(textureUrl);
        }} else {{
          texture = new THREE.Texture();
        }}
        
        texture.magFilter = THREE.NearestFilter;
        texture.minFilter = THREE.NearestFilter;

        const material = new THREE.MeshStandardMaterial({{
          map: texture,
          transparent: true,
          alphaTest: 0.1,
          roughness: 0.8,
          metalness: 0.1,
          wireframe: wireframeMode
        }});

        // 构建每个 Box Element
        if (data.elements) {{
          data.elements.forEach(elem => {{
            if (elem.export === false) return;
            const from = elem.from || [0, 0, 0];
            const to = elem.to || [1, 1, 1];
            const dx = Math.abs(to[0] - from[0]);
            const dy = Math.abs(to[1] - from[1]);
            const dz = Math.abs(to[2] - from[2]);

            const geom = new THREE.BoxGeometry(dx, dy, dz);
            
            // 自定义 UV 映射
            if (elem.faces) {{
              const uvAttr = geom.attributes.uv;
              // Three.js Box faces: 0,1 (+X east), 2,3 (-X west), 4,5 (+Y up), 6,7 (-Y down), 8,9 (+Z south), 10,11 (-Z north)
              const faceOrder = ['east', 'west', 'up', 'down', 'south', 'north'];
              
              faceOrder.forEach((fName, fIdx) => {{
                const fData = elem.faces[fName];
                if (fData && fData.uv) {{
                  const [u1, v1, u2, v2] = fData.uv;
                  const uMin = u1 / resWidth;
                  const uMax = u2 / resWidth;
                  const vMin = 1.0 - (v2 / resHeight);
                  const vMax = 1.0 - (v1 / resHeight);

                  const base = fIdx * 4;
                  uvAttr.setXY(base, uMin, vMax);
                  uvAttr.setXY(base + 1, uMax, vMax);
                  uvAttr.setXY(base + 2, uMin, vMin);
                  uvAttr.setXY(base + 3, uMax, vMin);
                }}
              }});
              uvAttr.needsUpdate = true;
            }}

            const mesh = new THREE.Mesh(geom, material);
            mesh.castShadow = true;
            mesh.receiveShadow = true;

            const cx = (from[0] + to[0]) / 2;
            const cy = (from[1] + to[1]) / 2;
            const cz = (from[2] + to[2]) / 2;

            if (elem.rotation && (elem.rotation[0] || elem.rotation[1] || elem.rotation[2])) {{
              const pivot = new THREE.Group();
              const ox = elem.origin ? elem.origin[0] : cx;
              const oy = elem.origin ? elem.origin[1] : cy;
              const oz = elem.origin ? elem.origin[2] : cz;

              pivot.position.set(ox, oy, oz);
              pivot.rotation.x = THREE.MathUtils.degToRad(elem.rotation[0] || 0);
              pivot.rotation.y = THREE.MathUtils.degToRad(elem.rotation[1] || 0);
              pivot.rotation.z = THREE.MathUtils.degToRad(elem.rotation[2] || 0);

              mesh.position.set(cx - ox, cy - oy, cz - oz);
              pivot.add(mesh);
              currentMeshGroup.add(pivot);
            }} else {{
              mesh.position.set(cx, cy, cz);
              currentMeshGroup.add(mesh);
            }}
          }});
        }}

        // 模型自动居中与缩放适配
        const box = new THREE.Box3().setFromObject(currentMeshGroup);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        currentMeshGroup.position.x = -center.x;
        currentMeshGroup.position.y = -box.min.y;
        currentMeshGroup.position.z = -center.z;

        scene.add(currentMeshGroup);

        const maxDim = Math.max(size.x, size.y, size.z, 10);
        camera.position.set(maxDim * 1.5, maxDim * 1.2, maxDim * 1.8);
        controls.target.set(0, size.y * 0.5, 0);
        controls.update();

      }} catch (err) {{
        console.error("加载 .bbmodel 失败:", err);
      }} finally {{
        loader.classList.remove('show');
      }}
    }}

    // 加载 FBX 格式模型
    function loadFBXFile(url, textureUrl) {{
      const loader = document.getElementById('stage-loader');
      loader.classList.add('show');

      if (currentMeshGroup) {{
        scene.remove(currentMeshGroup);
      }}

      const fbxLoader = new THREE.FBXLoader();
      fbxLoader.load(url, (object) => {{
        currentMeshGroup = object;
        
        let texture = null;
        if (textureUrl) {{
          texture = new THREE.TextureLoader().load(textureUrl);
          texture.magFilter = THREE.NearestFilter;
          texture.minFilter = THREE.NearestFilter;
        }}

        object.traverse((child) => {{
          if (child.isMesh) {{
            child.castShadow = true;
            child.receiveShadow = true;
            if (texture) {{
              child.material = new THREE.MeshStandardMaterial({{
                map: texture,
                roughness: 0.85,
                metalness: 0.05,
                side: THREE.DoubleSide,
                wireframe: wireframeMode
              }});
            }} else if (child.material) {{
              if (Array.isArray(child.material)) {{
                child.material.forEach(m => {{
                  m.side = THREE.DoubleSide;
                  m.wireframe = wireframeMode;
                }});
              }} else {{
                child.material.side = THREE.DoubleSide;
                child.material.wireframe = wireframeMode;
              }}
            }}
          }}
        }});

        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        
        object.position.x = -center.x;
        object.position.y = -box.min.y;
        object.position.z = -center.z;

        scene.add(object);

        const maxDim = Math.max(size.x, size.y, size.z, 10);
        camera.near = Math.min(0.5, maxDim / 100);
        camera.far = Math.max(8000, maxDim * 25);
        camera.updateProjectionMatrix();

        camera.position.set(maxDim * 1.5, maxDim * 1.1, maxDim * 1.6);
        controls.target.set(0, size.y * 0.45, 0);
        controls.maxDistance = maxDim * 12;
        controls.update();

        loader.classList.remove('show');
      }}, undefined, (err) => {{
        console.error("加载 FBX 失败:", err);
        loader.classList.remove('show');
      }});
    }}

    // 切换 3D 展示模型
    function selectModel(modelId) {{
      const model = GALLERY_DATA.models.find(m => m.id === modelId);
      if (!model) return;
      currentModel = model;

      // 更新卡片激活态
      document.querySelectorAll('.model-card').forEach(c => c.classList.remove('active'));
      const activeCard = document.getElementById('card_' + model.id);
      if (activeCard) activeCard.classList.add('active');

      // 更新舞台标题与描述
      document.getElementById('stage-model-title').innerHTML = `${{model.icon}} ${{model.title}}`;
      document.getElementById('stage-model-desc').textContent = model.desc || model.tag || '';
      document.getElementById('stage-format-text').textContent = `格式: .${{model.model_type.toUpperCase()}} | 贴图: ${{model.texture_file ? '已绑定' : '内置'}}`;

      // 3D 渲染器分发
      if (model.model_type === 'glb' || model.model_type === 'gltf') {{
        // Google model-viewer 引擎
        canvas.style.display = 'none';
        modelViewer.style.display = 'block';
        modelViewer.src = model.model_file;
      }} else {{
        // Three.js 引擎 (支持 .bbmodel 与 .fbx)
        modelViewer.style.display = 'none';
        canvas.style.display = 'block';
        if (model.model_type === 'bbmodel') {{
          loadBBModelFile(model.model_file, model.texture_file);
        }} else if (model.model_type === 'fbx') {{
          loadFBXFile(model.model_file, model.texture_file);
        }}
      }}

      // 更新右侧控制台
      renderConsolePanel(model);
    }}

    // 渲染右侧面板（角色 TTS 控制台 或 食物/建筑材质卡片）
    function renderConsolePanel(model) {{
      const consoleContainer = document.getElementById('console-scroll-content');
      const consoleTitle = document.getElementById('console-panel-title');
      const consoleBadge = document.getElementById('console-mode-badge');

      if (model.category === 'characters') {{
        consoleTitle.innerHTML = `<span>🎙️</span> ${{model.name}} 专属语音`;
        consoleBadge.textContent = 'KOKORO 0.8x 原声';
        consoleBadge.style.color = 'var(--accent-green)';

        const ttsInfo = model.tts_key ? GALLERY_DATA.tts[model.tts_key] : null;

        if (!ttsInfo || !ttsInfo.actions || Object.keys(ttsInfo.actions).length === 0) {{
          consoleContainer.innerHTML = `
            <div class="character-profile-card">
              <div class="profile-top">
                <span class="profile-name">${{model.title}}</span>
                <span class="profile-tag">${{model.tag}}</span>
              </div>
              <p class="profile-desc">${{model.desc}}</p>
            </div>
            <div style="text-align: center; padding: 40px 20px; color: var(--text-muted);">
              <div style="font-size: 32px; margin-bottom: 8px;">🔇</div>
              <p>该角色暂无配置本地语音包</p>
            </div>
          `;
          return;
        }}

        // 构建语音操作区
        let html = `
          <div class="character-profile-card">
            <div class="profile-top">
              <span class="profile-name">${{model.title}}</span>
              <span class="profile-tag">${{model.tag}}</span>
            </div>
            <p class="profile-desc">${{model.desc}}</p>
          </div>
        `;

        const actionIcons = {{
          '点餐 A': '🥩',
          '点餐 B': '🍖',
          '点餐 C': '🍗',
          '满意': '✨',
          '不满意': '💢'
        }};

        Object.keys(ttsInfo.actions).forEach(actionName => {{
          const act = ttsInfo.actions[actionName];
          const icon = actionIcons[actionName] || '🎙️';
          const condTag = act.condition ? act.condition : '判定状态';

          html += `
            <div class="action-group-card">
              <div class="action-header">
                <span class="action-title">${{icon}} ${{actionName}}</span>
                <span class="action-cond">${{condTag}}</span>
              </div>
              <div class="lang-btn-grid">
          `;

          const langs = [
            {{ key: 'CN', label: '中文', flag: '🇨🇳' }},
            {{ key: 'ES', label: '西语', flag: '🇪🇸' }},
            {{ key: 'US', label: '英语', flag: '🇺🇸' }}
          ];

          langs.forEach(l => {{
            const lData = act.languages[l.key];
            if (lData && lData.wav) {{
              const voiceTip = lData.voice ? `${{lData.voice}}` : '';
              html += `
                <button class="voice-btn" id="vbtn_${{model.id}}_${{actionName}}_${{l.key}}"
                  onclick="playTTSAudio('${{lData.wav}}', '${{escapeQuotes(lData.subtitle)}}', '${{escapeQuotes(lData.tts_text)}}', '${{l.flag}} ${{l.label}}', '${{voiceTip}}', '${{act.condition}}', this)">
                  <span class="lang-flag">${{l.flag}}</span>
                  <span class="lang-label">${{l.label}}</span>
                </button>
              `;
            }} else {{
              html += `
                <button class="voice-btn" disabled style="opacity: 0.35;">
                  <span class="lang-flag">${{l.flag}}</span>
                  <span class="lang-label">${{l.label}}</span>
                </button>
              `;
            }}
          }});

          html += `
              </div>
            </div>
          `;
        }});

        consoleContainer.innerHTML = html;

      }} else {{
        // 食物或建筑展示面板
        consoleTitle.innerHTML = `<span>📋</span> 资产材质详情`;
        consoleBadge.textContent = '3D ASSET';
        consoleBadge.style.color = 'var(--accent-orange)';

        consoleContainer.innerHTML = `
          <div class="character-profile-card">
            <div class="profile-top">
              <span class="profile-name">${{model.title}}</span>
              <span class="profile-tag">${{model.tag}}</span>
            </div>
            <p class="profile-desc">${{model.desc}}</p>
          </div>

          <div class="asset-detail-card">
            <div class="detail-row">
              <span class="detail-label">资产分类</span>
              <span class="detail-val">${{model.category.toUpperCase()}}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">模型源文件</span>
              <span class="detail-val">${{model.model_file ? model.model_file.split('/').pop() : '无'}}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">渲染格式</span>
              <span class="detail-val">.${{model.model_type.toUpperCase()}}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">贴图文件</span>
              <span class="detail-val">${{model.texture_file ? model.texture_file.split('/').pop() : '内置材质'}}</span>
            </div>

            ${{model.texture_file ? `
              <div class="texture-preview-box">
                <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">像素纹理贴图预览 (64x64/128x128)</div>
                <img src="${{model.texture_file}}" alt="贴图">
              </div>
            ` : ''}}
          </div>
        `;
      }}
    }}

    function escapeQuotes(str) {{
      if (!str) return '';
      return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
    }}

    // 播放 TTS 音频并驱动字幕
    function playTTSAudio(wavUrl, subtitle, ttsText, langLabel, voiceTip, condition, btnEl) {{
      if (!wavUrl) return;

      // 切换按钮高亮态
      if (currentActiveVoiceBtn) {{
        currentActiveVoiceBtn.classList.remove('playing');
      }}
      if (btnEl) {{
        btnEl.classList.add('playing');
        currentActiveVoiceBtn = btnEl;
      }}

      // 显示字幕横幅
      const banner = document.getElementById('now-playing-banner');
      banner.style.display = 'flex';

      document.getElementById('playing-lang-tag').textContent = langLabel + ' 正在播放';
      document.getElementById('playing-voice-badge').textContent = voiceTip ? `${{voiceTip}} · 0.8x` : '0.8x';
      document.getElementById('playing-sub-text').textContent = subtitle ? `“${{subtitle}}”` : '“暂无字幕”';
      document.getElementById('playing-tts-text').textContent = ttsText ? `TTS 拼读注音: ${{ttsText}}` : '';
      document.getElementById('playing-meta-text').textContent = condition ? `触发判定条件: ${{condition}}` : '';

      // 播放音频
      audioPlayer.src = wavUrl;
      audioPlayer.play().catch(e => console.log('Audio autoplay prevented:', e));

      audioPlayer.onended = () => {{
        if (currentActiveVoiceBtn) {{
          currentActiveVoiceBtn.classList.remove('playing');
          currentActiveVoiceBtn = null;
        }}
      }};
    }}

    // 切换主分类
    function switchCategory(cat) {{
      currentCategory = cat;
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.querySelector(`.tab-${{cat}}`);
      if (activeBtn) activeBtn.classList.add('active');

      const titleMap = {{
        'characters': '<span>👤</span> 角色列表',
        'food': '<span>🍖</span> 食物列表',
        'buildings': '<span>🏠</span> 建筑设施列表'
      }};
      document.getElementById('list-panel-title').innerHTML = titleMap[cat] || '模型列表';

      renderModelList();
    }}

    // 渲染左侧模型列表
    function renderModelList(filterText = '') {{
      const container = document.getElementById('model-item-list');
      const filtered = GALLERY_DATA.models.filter(m => {{
        const matchCat = m.category === currentCategory;
        const matchSearch = filterText === '' || 
          m.title.toLowerCase().includes(filterText.toLowerCase()) || 
          m.name.toLowerCase().includes(filterText.toLowerCase()) ||
          m.tag.toLowerCase().includes(filterText.toLowerCase());
        return matchCat && matchSearch;
      }});

      document.getElementById('list-count-badge').textContent = `${{filtered.length}} 项`;

      if (filtered.length === 0) {{
        container.innerHTML = `
          <div style="text-align: center; padding: 40px 10px; color: var(--text-muted);">
            <p>未找到匹配的模型</p>
          </div>
        `;
        return;
      }}

      let html = '';
      filtered.forEach(m => {{
        const isActive = currentModel && currentModel.id === m.id;
        const imgIcon = m.preview_file ? `<img src="${{m.preview_file}}" alt="">` : m.icon;

        html += `
          <div class="model-card ${{isActive ? 'active' : ''}}" id="card_${{m.id}}" onclick="selectModel('${{m.id}}')">
            <div class="card-icon-wrap">
              ${{imgIcon}}
            </div>
            <div class="card-info">
              <div class="card-title">${{m.title}}</div>
              <div class="card-sub">${{m.tag || m.desc}}</div>
            </div>
            <div class="card-badge">${{m.model_type}}</div>
          </div>
        `;
      }});

      container.innerHTML = html;

      // 如果当前没有选中模型，自动选中当前分类的第一个
      if (!currentModel || currentModel.category !== currentCategory) {{
        if (filtered.length > 0) {{
          selectModel(filtered[0].id);
        }}
      }}
    }}

    function handleSearch(val) {{
      renderModelList(val.trim());
    }}

    function toggleAutoRotate() {{
      autoRotate = !autoRotate;
      controls.autoRotate = autoRotate;
      if (modelViewer) modelViewer.autoRotate = autoRotate;
      document.getElementById('btn-autorotate').classList.toggle('active', autoRotate);
    }}

    function toggleWireframe() {{
      wireframeMode = !wireframeMode;
      document.getElementById('btn-wireframe').classList.toggle('active', wireframeMode);
      if (currentMeshGroup) {{
        currentMeshGroup.traverse(child => {{
          if (child.isMesh && child.material) {{
            child.material.wireframe = wireframeMode;
          }}
        }});
      }}
    }}

    function resetCamera() {{
      if (currentMeshGroup) {{
        const box = new THREE.Box3().setFromObject(currentMeshGroup);
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z, 10);
        camera.position.set(maxDim * 1.5, maxDim * 1.2, maxDim * 1.8);
        controls.target.set(0, size.y * 0.5, 0);
        controls.update();
      }}
      if (modelViewer) {{
        modelViewer.cameraOrbit = '0deg 75deg 105%';
      }}
    }}

    // 初始化运行
    window.addEventListener('DOMContentLoaded', () => {{
      initThreeScene();
      
      // 更新顶部统计数据
      document.getElementById('stat-model-count').textContent = `${{GALLERY_DATA.models.length}} 个模型`;
      
      let totalWavs = 0;
      Object.values(GALLERY_DATA.tts).forEach(c => {{
        if (c.actions) {{
          Object.values(c.actions).forEach(a => {{
            if (a.languages) {{
              Object.values(a.languages).forEach(l => {{
                if (l.wav) totalWavs++;
              }});
            }}
          }});
        }}
      }});
      document.getElementById('stat-voice-count').textContent = `${{totalWavs}} 条 (3语)`;

      // 默认展示角色分类
      switchCategory('characters');
    }});
  </script>
</body>
</html>
"""
    return html

def ensure_patched_fbx_loader(script_dir):
    loader_path = os.path.join(script_dir, 'three_fbx_loader.js')
    if os.path.exists(loader_path) and os.path.getsize(loader_path) > 10000:
        return
    import urllib.request
    url = 'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/FBXLoader.js'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.read().decode('utf-8')
        code = code.replace(
            'function isFbxFormatASCII( text ) {',
            'function isFbxFormatASCII( text ) {\n\t\treturn true; // Patched for Blockbench ASCII FBX'
        )
        code = code.replace(
            'const parentName = currentNode.name;',
            'if ( ! currentNode ) return;\n\t\t\tconst parentName = currentNode.name; // Patched for top-level properties'
        )
        with open(loader_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print("✅ 成功生成热修复版 three_fbx_loader.js")
    except Exception as e:
        print(f"⚠️ 下载并修复 FBXLoader 失败: {e}")

def main():
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    print("=" * 60)
    print("🚀 开始构建 3D 模型与 TTS 语音展示网页...")
    print(f"工作根目录: {root_dir}")
    print(f"脚本所在目录: {script_dir}")
    print("=" * 60)
    
    # 确保修复版 FBXLoader 存在
    ensure_patched_fbx_loader(script_dir)
    
    # 扫描数据
    data = scan_gallery_data(root_dir)
    print(f"✅ 成功扫描到 {len(data['models'])} 个 3D 模型资产:")
    char_count = len([m for m in data['models'] if m['category'] == 'characters'])
    food_count = len([m for m in data['models'] if m['category'] == 'food'])
    bld_count = len([m for m in data['models'] if m['category'] == 'buildings'])
    print(f"   - 角色模型: {char_count} 个")
    print(f"   - 食物模型: {food_count} 个")
    print(f"   - 建筑模型: {bld_count} 个")
    
    tts_count = len(data['tts'])
    total_wavs = sum(
        len(a.get('languages', {}))
        for c in data['tts'].values()
        for a in c.get('actions', {}).values()
    )
    print(f"✅ 成功关联 {tts_count} 个角色的语音数据，共包含 {total_wavs} 条语音切片。")
    
    # 生成 HTML 内容
    html_content = generate_html_content(data)
    
    # 严格写入根目录 index.html
    output_html_path = os.path.join(root_dir, 'index.html')
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"🎉 成功生成展示网页: {output_html_path}")
    print(f"   文件大小: {os.path.getsize(output_html_path)} 字节")
    print("=" * 60)
    print("✨ 你可以直接在浏览器中打开根目录下的 index.html 查看展示网页！")

if __name__ == '__main__':
    main()
