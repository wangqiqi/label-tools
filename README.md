# 数据标注工具汇总

本仓库整理了主流的开源数据标注工具，涵盖计算机视觉（CV）、自然语言处理（NLP）、点云和文本等多个领域。

## 📋 目录

- [综合类标注工具](#综合类标注工具)
- [计算机视觉（CV）专用工具](#计算机视觉cv专用工具)
- [自然语言处理（NLP）专用工具](#自然语言处理nlp专用工具)
- [点云（Point Cloud）专用工具](#点云point-cloud专用工具)
- [服务端/自托管平台](#服务端自托管平台)
- [轻量级/嵌入式工具](#轻量级嵌入式工具)
- [商业平台（支持自托管）](#商业平台支持自托管)
- [医学影像专用工具](#医学影像专用工具)
- [多模态标注平台](#多模态标注平台)
- [其他专用工具](#其他专用工具)
- [工具选择建议](#工具选择建议)
- [行业趋势与展望](#行业趋势与展望)

---

## 综合类标注工具

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| Label Studio | [github.com/HumanSignal/label-studio](https://github.com/HumanSignal/label-studio) | 20k+ stars / 2.5k+ forks | Apache-2.0 | Python, React | CV, NLP, Audio, Video, Text, Time-series | 最灵活的多模态标注平台，支持图像、文本、音频、视频等多种数据类型，提供标准化输出格式，适合企业级应用 |
| CVAT | [github.com/cvat-ai/cvat](https://github.com/cvat-ai/cvat) | 14k+ stars / 3k+ forks | MIT | Python, Django, React | CV, Video, Image | 业界领先的计算机视觉标注工具，支持图像和视频标注，提供自动标注、跟踪等高级功能，适合任何规模的团队 |
| Labelme | [github.com/wkentaro/labelme](https://github.com/wkentaro/labelme) | 13k+ stars / 3.5k+ forks | GPLv3 | Python, Qt | CV, Image | Python 图像多边形标注工具，支持多边形、矩形、圆形、线条、点和图像级标注，轻量级且易于使用 |
| LabelImg | [github.com/HumanSignal/labelImg](https://github.com/HumanSignal/labelImg) | 23k+ stars / 6.4k+ forks | MIT | Python, Qt | CV, Image | 经典的图像边界框标注工具，专注于目标检测任务，支持 PASCAL VOC 和 YOLO 格式，现已并入 Label Studio 社区 |
| Supervisely | [supervisely.com](https://supervisely.com) | 商业产品（部分开源） | 专有 | Python, Web | CV, Video, Image, Point Cloud | 端到端计算机视觉平台，支持图像、视频和点云标注，提供深度学习集成和协作功能 |

## 计算机视觉（CV）专用工具

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| AnyLabeling | [github.com/vietanhdev/anylabeling](https://github.com/vietanhdev/anylabeling) | 7k+ stars / 800+ forks | GPLv3 | Python, Qt | CV, Image, Video | AI 辅助标注工具，集成 YOLO、SAM、SAM2 和 MobileSAM，支持自动标注和多种标注类型 |
| X-AnyLabeling | [github.com/CVHub520/X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) | 5k+ stars / 500+ forks | GPLv3 | Python, Qt | CV, Image, OCR | 增强版 AnyLabeling，支持 Segment Anything 和多种 AI 模型，专注于工业级自动标注 |
| makesense.ai | [makesense.ai](https://makesense.ai) | 3k+ stars | GPLv3 | TypeScript, React | CV, Image | 免费在线图像标注工具，无需安装，支持目标检测、图像分类和语义分割，适合快速原型开发 |
| COCO Annotator | [github.com/jsbroks/coco-annotator](https://github.com/jsbroks/coco-annotator) | 3k+ stars / 700+ forks | MIT | Python, Vue.js | CV, Image | Web 图像分割标注工具，专为目标检测、定位和关键点标注设计，输出 COCO 格式 |
| VGG Image Annotator (VIA) | [gitlab.com/vgg/via](https://gitlab.com/vgg/via) | 2.5k+ stars | BSD-2-Clause | JavaScript | CV, Image, Video | 轻量级的图像和视频标注工具，完全在浏览器中运行，支持多种标注类型 |
| VoTT | [github.com/microsoft/VoTT](https://github.com/microsoft/VoTT) | 4.5k+ stars / 1k+ forks | MIT | TypeScript, React, Electron | CV, Image, Video | 微软开源的视觉对象标注工具，Electron 应用，支持端到端目标检测模型构建（已归档，不再维护） |
| Sloth | [github.com/cvhciKIT/sloth](https://github.com/cvhciKIT/sloth) | 1k+ stars / 300+ forks | MIT | Python, Qt | CV, Image, Video | 图像和视频数据标注工具，专为计算机视觉研究设计，支持自定义标注类型 |
| Yolo_mark | [github.com/AlexeyAB/Yolo_mark](https://github.com/AlexeyAB/Yolo_mark) | 1.5k+ stars / 600+ forks | MIT | C++, OpenCV | CV, Image | YOLO 专用标注工具，GUI 界面，用于标注边界框训练 Darknet YOLO 模型 |
| ImgLab | [github.com/NaturalIntelligence/imglab](https://github.com/NaturalIntelligence/imglab) | 1k+ stars / 200+ forks | MIT | JavaScript, Vue.js | CV, Image | Web 图像标注工具，支持多种格式，可用于训练 dlib 或其他目标检测器 |
| JS Segment Annotator | [github.com/kyamagu/js-segment-annotator](https://github.com/kyamagu/js-segment-annotator) | 521+ stars / 159+ forks | BSD-3-Clause | JavaScript | CV, Image | 基于图像分割的 JavaScript 标注工具，纯前端实现，支持区域标注 |
| RectLabel | [rectlabel.com](https://rectlabel.com) | 商业产品 | 专有 | Swift, macOS | CV, Image | macOS 专用离线图像标注工具，支持边界框、多边形、关键点等，输出 COCO/YOLO/VOC 格式 |
| Roboflow Annotate | [roboflow.com/annotate](https://roboflow.com/annotate) | 商业产品（部分开源） | 专有 | Web, AI | CV, Image, Video | AI 辅助标注工具，支持自动标注和主动学习，可利用 50,000+ 公开模型加速标注过程 |

## 自然语言处理（NLP）专用工具

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| doccano | [github.com/doccano/doccano](https://github.com/doccano/doccano) | 9.5k+ stars / 1.8k+ forks | MIT | Python, Django, Vue.js | NLP, Text | 开源文本标注工具，专为 NLP 任务设计，支持序列标注、文本分类、序列到序列任务等 |
| brat | [github.com/nlplab/brat](https://github.com/nlplab/brat) | 1.8k+ stars / 500+ forks | MIT | Python, JavaScript | NLP, Text | 快速标注工具，基于 Web 的文本标注、可视化和编辑工具，专为结构化标注设计，支持 NLP 辅助 |
| WebAnno | [github.com/webanno/webanno](https://github.com/webanno/webanno) | 800+ stars / 200+ forks | Apache-2.0 | Java, Spring | NLP, Text | 通用 Web 文本标注工具，支持多种语言学标注，现已迁移到 INCEpTION 项目 |
| ActiveTigger | [github.com/emilienschultz/activetigger](https://github.com/emilienschultz/activetigger) | 开源项目 | 开源 | Python, BERT | NLP, Text | 为计算社会科学研究设计的轻量级文本标注工具，集成微调模型和主动学习，支持 LLM 即服务进行提示式标注 |
| tagtog | [tagtog 文档](https://docs.tagtog.com) | 商业产品 | 专有 | Web | NLP, Text, NER | Web 文本标注工具，专注于语义标注和 NER，支持协作和自动标注（官网访问受限） |
| Prodigy | [prodi.gy](https://prodi.gy) | 商业产品 | 专有 | Python | NLP, Text, Image | 由 spaCy 团队开发的高效标注工具，支持主动学习，可与 Python 工作流深度集成，适合快速迭代 |
| Argilla | [github.com/argilla-io/argilla](https://github.com/argilla-io/argilla) | 3.5k+ stars / 350+ forks | Apache-2.0 | Python, FastAPI, Vue.js | NLP, Text, LLM | 面向 LLM 和 NLP 的协作标注平台，支持数据质量监控和模型评估 |
| LabelLLM | [github.com/opendatalab/LabelLLM](https://github.com/opendatalab/LabelLLM) | 1k+ stars / 100+ forks | Apache-2.0 | Python, Vue.js | NLP, Text, LLM | 专为大语言模型设计的开源标注平台，支持对话、指令等多种 LLM 数据标注 |

## 点云（Point Cloud）专用工具

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| labelCloud | [github.com/ch-sa/labelCloud](https://github.com/ch-sa/labelCloud) | 800+ stars / 150+ forks | GPLv3 | Python, Qt | Point Cloud, 3D | 轻量级 3D 点云边界框标注工具，支持多种点云格式，界面友好 |
| SUSTechPOINTS | [github.com/naurril/SUSTechPOINTS](https://github.com/naurril/SUSTechPOINTS) | 500+ stars / 120+ forks | MIT | Python, Qt | Point Cloud, 3D | 专为自动驾驶设计的 3D 点云标注平台，支持激光雷达数据标注 |
| 3D Annotation Tool | [github.com/strayrobots/3d-annotation-tool](https://github.com/strayrobots/3d-annotation-tool) | 300+ stars / 60+ forks | MIT | Python, Three.js | Point Cloud, 3D | 图形化 3D 点云和数据标注工具，支持多种 3D 数据格式 |
| Supervisely Point Cloud | [github.com/supervisely-ecosystem/pointcloud-labeling-tool](https://github.com/supervisely-ecosystem/pointcloud-labeling-tool) | 200+ stars / 40+ forks | MIT | Python, Web | Point Cloud, 3D, Video | 支持激光雷达/雷达传感器的综合 3D 场景标注，带 AI 目标跟踪和点云分割功能 |
| Kognic Platform | [kognic.com](https://www.kognic.com) | 商业产品 | 专有 | Web, AI | Point Cloud, 3D, Semantic Segmentation | 专注于自动驾驶和机器人的企业级平台，支持 3D 语义/实例分割质量分析和程序化检查（2026年1月更新） |

## 服务端/自托管平台

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| Diffgram | [github.com/diffgram/diffgram](https://github.com/diffgram/diffgram) | 1.8k+ stars / 300+ forks | MIT | Python, Vue.js | CV, NLP, Multi-modal | AI 数据存储平台，支持模式、预测和人工监督，可自托管部署，提供完整的数据工作流 |
| INCEpTION | [github.com/inception-project/inception](https://github.com/inception-project/inception) | 800+ stars / 200+ forks | Apache-2.0 | Java, Spring | NLP, Text | 语义标注平台，提供智能标注辅助和知识管理，支持自托管部署，适合学术研究和企业应用 |
| Tator | [github.com/cvisionai/Tator-Native](https://github.com/cvisionai/Tator-Native) | 34+ stars / 7+ forks | AGPL-3.0 | C++, Qt | CV, Video, Image | 视频分析 Web 平台，支持大规模视频和图像标注，提供 AI 辅助标注和自定义工作流（已归档，被 Tator Online 取代） |
| Scalabel | [github.com/scalabel/scalabel](https://github.com/scalabel/scalabel) | 543+ stars / 112+ forks | Apache-2.0 | TypeScript, React | CV, 2D, 3D | 多功能 Web 标注工具，支持 2D 和 3D 数据标注，BDD100K 数据集使用此工具标注 |
| LabelFlow | [github.com/labelflow/labelflow](https://github.com/labelflow/labelflow) | 500+ stars / 80+ forks | AGPL-3.0 | TypeScript, Next.js | CV, Image | 开放的图像标注平台，支持协作和自托管，提供现代化的 Web 界面 |
| Ango Hub | [imerit.net/ango-hub](https://imerit.net/ango-hub) | 商业产品（部分开源） | 专有 | Web | CV, NLP, Multi-modal | 数据标注和模型微调平台，支持多传感器融合和 3D 标注，适合自动驾驶等生产级应用 |

## 轻量级/嵌入式工具

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| Universal Data Tool | [github.com/UniversalDataTool/universal-data-tool](https://github.com/UniversalDataTool/universal-data-tool) | 2k+ stars / 200+ forks | MIT | JavaScript, React | CV, NLP, Text, Image | 通用数据标注工具，支持多种数据类型，提供 Web 界面和桌面应用，易于协作 |
| Annotorious | [github.com/annotorious/annotorious](https://github.com/annotorious/annotorious) | 1.5k+ stars / 200+ forks | BSD-3-Clause | JavaScript | Image, Web | JavaScript 图像标注库，只需几行代码即可为网页添加标注功能，轻量级且易于集成 |
| Recogito | [github.com/recogito/recogito-js](https://github.com/recogito/recogito-js) | 800+ stars / 100+ forks | BSD-3-Clause | JavaScript | Text, Image | 文本和图像交互式标注 JavaScript 库，支持协作标注，适合数字人文项目 |
| Pigeon | [github.com/agermanidis/pigeon](https://github.com/agermanidis/pigeon) | 700+ stars / 100+ forks | Apache-2.0 | Python, Jupyter | Jupyter, Text, Image | Jupyter Notebook 标注小部件，快速标注数据集，支持文本、图像和回归任务 |
| ipyannotations | [pypi.org/project/ipyannotations](https://pypi.org/project/ipyannotations) | 200+ stars / 30+ forks | MIT | Python, Jupyter | Jupyter, Image | Jupyter 富标注库，专为图像数据设计，提供交互式标注界面 |

## 商业平台（支持自托管）

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| V7 Darwin | [v7labs.com](https://www.v7labs.com) | 商业产品 | 专有 | Web, AI | CV, Video, Image, Medical | 企业级视觉 AI 平台，支持 SAM 3 自动分割，提供视频标注和医学影像（DICOM）标注，适合生产环境 |
| Encord | [encord.com](https://encord.com) | 商业产品 | 专有 | Web, AI | CV, NLP, Multi-modal, 3D, LiDAR | AI 辅助数据标注平台，支持图像、视频、音频、文档、3D 和 LiDAR 数据，提供 HITL 工作流 |
| SuperAnnotate | [superannotate.com](https://www.superannotate.com) | 商业产品 | 专有 | Web, AI | CV, NLP, Multi-modal | 端到端数据标注平台，支持主动学习和数据管理，提供质量控制和团队协作功能 |
| Scale AI | [scale.com](https://scale.com) | 商业产品 | 专有 | Web, AI | CV, NLP, Multi-modal | 领先的 AI 数据平台，提供高质量标注服务和工具，支持大规模数据处理 |
| Segments.ai | [segments.ai](https://segments.ai) | 商业产品 | 专有 | Web | CV, 2D, 3D, Point Cloud | 多传感器数据标注平台，支持 2D 图像和 3D 点云同步标注，适合机器人和自动驾驶（YC W21，网站有反爬虫保护） |
| Labellerr | [labellerr.com](https://www.labellerr.com) | 商业产品 | 专有 | Web, AI | CV, NLP, Video | 数据标注平台，支持自托管，提供 AI 辅助标注，声称可减少 80% 标注时间 |
| VisionRepo | [averroes.ai](https://averroes.ai) | 商业产品 | 专有 | Web | CV, Image, Video | 数据标注和视觉数据管理平台，支持 AI 辅助工作流和数据版本控制 |
| Playment | [YC 公司页面](https://www.ycombinator.com/companies/playment) | 商业产品 | 专有 | Web | CV, Image, Video, Sensor | 全托管数据标注平台，专注于自动驾驶、无人机和地图等领域（2021年被 TELUS International 收购） |
| Hive Data | [thehive.ai](https://thehive.ai) | 商业产品 | 专有 | Web, AI | CV, NLP, Multi-modal | AI 数据标注和内容审核平台，支持图像、视频和文本标注 |
| Kili Technology | [kili-technology.com](https://kili-technology.com) | 商业产品 | 专有 | Web, AI | CV, NLP, Video, Geospatial | 企业级标注平台，支持本地部署，提供多模态标注、质量控制和协作功能。2026年1月更新：增强批量标注管理（提速60%）和节点编辑器，适合国防、医疗、农业监测等领域 |
| Hasty (CloudFactory) | [cloudfactory.com/hasty](https://www.cloudfactory.com/platform/ai-cv-tool) | 商业产品 | 专有 | Web, AI | CV, Image, Video | AI 驱动的视觉标注工具，可自动化 90% 的质量控制任务，随使用越来越快 |
| Dataloop | [dataloop.ai](https://dataloop.ai) | 商业产品 | 专有 | Web, AI | CV, NLP, Multi-modal | 端到端数据管理和标注平台，支持自托管，提供 MLOps 集成 |
| Labelbox | [labelbox.com](https://labelbox.com) | 商业产品 | 专有 | Web, AI | CV, NLP, Multi-modal | 领先的训练数据平台，支持企业级部署，提供完整的数据管理和标注解决方案 |
| Dataturks | [GitHub 归档](https://github.com/DataTurks) | 已停止维护 | Apache-2.0 | Java, Web | CV, NLP, Text, Image | 人机协作标注平台，支持图像、视频和文本标注（项目已归档，网站已下线） |

## 医学影像专用工具

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| NimbusImage | [nimbusimage.com](https://docs.nimbusimage.com/new-features) | 商业产品 | 专有 | Web, AI | Medical Imaging, Biology | 面向科研的生物影像标注和分析平台，支持圆形/椭圆标注、合并多边形、SAM1/SAM2 辅助分割（2026年2月更新） |
| Cytomine | [cytomine.org](https://cytomine.org) | 开源项目 | Apache-2.0 | Java, Groovy, JavaScript | Pathology, Whole-slide | 开源的大规模病理学图像协作标注平台，集成 AI 辅助细胞/区域标注和基于内容的图像检索（CBIR），适合数字病理学 |

## 多模态标注平台

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| AutoDive+ | [论文链接](https://dl.acm.org/doi/10.1145/3701716.3715167) | 学术研究 | 研究项目 | Python, AI | Multi-modal, PDF | 增强版多模态在线标注工具，支持 PDF 文档直接标注，通过主动学习提高效率，适合材料科学、生物合成等领域 |
| Appen 多模态工具 | [appen.com](https://tw.appendata.com/blogs/multimodal-labeling-tool) | 商业产品 | 专有 | Web, AI | Multi-modal, Semantic | 专业多模态标注平台，支持语义层级的跨模态关联（如将文字描述关联到影像区域），适合医疗 AI、智能客服等场景 |

## 其他专用工具

| 名称 | 地址 | Star/Fork 数 | 开源协议 | 技术栈 | 支持类型 | 说明 |
|------|------|-------------|---------|---------|---------|------|
| Cleanlab | [github.com/cleanlab/cleanlab](https://github.com/cleanlab/cleanlab) | 9k+ stars / 700+ forks | AGPL-3.0 | Python | Data Quality | 数据中心 AI 包，专注于数据质量和标签清洗，适合处理混乱的真实世界数据 |
| LabelConvert | [github.com/RapidAI/LabelConvert](https://github.com/RapidAI/LabelConvert) | 500+ stars / 100+ forks | Apache-2.0 | Python | Format Conversion | 数据集格式转换工具，支持 labelme、labelImg、YOLO、VOC、COCO 等格式互转 |
| AURA | [arXiv:2602.02564](https://arxiv.org/abs/2602.02564) | 学术研究 | 研究项目 | Python, AI Agents | Automated Annotation | 代理式 AI 框架，通过协调多个 AI 智能体生成和验证标签，代表自动化高可靠性数据标注的前沿方向 |

---

## 工具选择建议

### 按使用场景选择：

1. **多模态项目**：Label Studio、Encord 或 Appen 多模态工具 - 支持最全面的数据类型和跨模态关联
2. **计算机视觉**：CVAT 或 V7 Darwin - 功能最强大，社区活跃
3. **快速原型**：makesense.ai 或 Labelme - 轻量级，易上手
4. **NLP 任务**：doccano 或 brat - 专为文本标注优化
5. **计算社会科学**：ActiveTigger - 集成主动学习和 LLM，适合学术研究
6. **点云标注**：labelCloud - 界面友好，支持多种格式
7. **自动驾驶多传感器**：Kognic Platform 或 SUSTechPOINTS - 专为激光雷达和 3D 分割设计
8. **LLM 数据准备**：LabelLLM 或 Argilla - 专为大模型优化
9. **视频标注**：Tator、CVAT 或 V7 Darwin - 支持大规模视频处理
10. **学术研究**：INCEpTION 或 brat - 语义标注和知识管理
11. **Jupyter 环境**：Pigeon 或 ipyannotations - 直接在 Notebook 中标注
12. **Web 集成**：Annotorious 或 Recogito - 轻量级 JavaScript 库
13. **YOLO 训练**：Yolo_mark 或 LabelImg - 专为 YOLO 格式优化
14. **COCO 格式**：COCO Annotator - 输出标准 COCO 格式
15. **医学影像**：V7 Darwin、Encord、NimbusImage 或 Cytomine - 支持 DICOM、病理切片等专业格式
16. **数字病理学**：Cytomine - 专为大规模病理图像设计，支持 AI 辅助和 CBIR
17. **生物影像研究**：NimbusImage - 支持 SAM 辅助分割和批量标注计算
18. **macOS 用户**：RectLabel - 原生 macOS 应用
19. **PDF 文档标注**：AutoDive+ - 支持多模态文档直接标注

### 按部署方式选择：

- **纯本地工具**：Labelme, LabelImg, labelCloud, Yolo_mark, RectLabel
- **浏览器工具**：makesense.ai, Annotorious, VIA
- **自托管服务端**：Label Studio, CVAT, doccano, INCEpTION, Tator, Scalabel, COCO Annotator, Diffgram
- **Jupyter 集成**：Pigeon, ipyannotations
- **商业自托管**：V7 Darwin, Encord, Kili Technology, Dataloop, Labelbox, SuperAnnotate

### 按团队规模选择：

- **个人/小团队**：Labelme, LabelImg, makesense.ai, Pigeon, Yolo_mark, RectLabel
- **中型团队**：doccano, labelCloud, CVAT, Universal Data Tool, COCO Annotator, Sloth
- **企业级**：Label Studio, CVAT (企业版), V7 Darwin, Encord, Kili Technology, Ango Hub, SuperAnnotate, Scale AI, Kognic

---

## 📊 统计概览

- **总计工具数**：60+ 个
- **开源工具**：38+ 个
- **商业产品**：18+ 个
- **学术研究项目**：3 个
- **支持 CV**：38+ 个
- **支持 NLP**：16+ 个
- **支持点云**：7 个
- **医学影像**：4 个
- **多模态**：4 个
- **支持自托管**：22+ 个
- **AI 辅助标注**：20+ 个

---

## 🔮 行业趋势与展望

### 1. 代理式 AI（Agentic AI）在自动标注领域的探索

以 AURA 为代表的代理式 AI 框架，通过协调多个 AI 智能体来生成和验证标签，并使用概率模型推断真实标签和智能体可靠性。这代表了利用多智能体协作和统计方法进行自动化、高可靠性数据标注的前沿方向。

### 2. 多模态标注的深度发展

多模态标注正在从"支持多种格式"向"建立语义关联"深度发展。新一代工具（如 Appen 多模态工具）支持在统一画布上将文字描述直接关联到影像区域或视频特定帧，为训练具备深层理解力的多模态模型提供高质量数据。

### 3. 主动学习与 AI 辅助标注的普及

越来越多的工具（如 ActiveTigger、Prodigy、Roboflow）集成主动学习和 AI 辅助功能，通过智能推荐最有价值的样本进行标注，显著提高标注效率。预计未来这将成为标注工具的标配功能。

### 4. 垂直领域专业化

针对特定领域的专业标注工具不断涌现：
- **医学影像**：Cytomine、NimbusImage 等专注于病理学和生物影像
- **自动驾驶**：Kognic 等提供 3D 语义分割和程序化质量检查
- **计算社会科学**：ActiveTigger 等集成 LLM 和主动学习

### 5. 质量控制与程序化检查

企业级平台（如 Kognic、Kili Technology）引入程序化检查功能，自动验证标注的几何属性、一致性等，大幅提升数据质量和标注效率。

---

## 🤝 贡献

欢迎提交 Issue 或 Pull Request 来补充更多标注工具或更新现有信息。

## 📝 数据来源说明

本文档中的 Star/Fork 数据为近期统计的大致数值（截至 2026年2月），实际数据可能有所变化。所有信息均来自公开渠道，包括 GitHub、官方网站、学术论文等。

---

**最后更新时间**：2026年2月

**参考来源**：
- [GitHub Topics - Data Labeling](https://github.com/topics/data-labeling)
- [GitHub Topics - 3D Annotation](https://github.com/topics/3d-annotation)
- 各工具官方仓库和文档

## ⭐ Star History

如果这个仓库对你有帮助，欢迎 Star ⭐

## 📄 License

本仓库采用 [MIT License](LICENSE) 开源协议。
