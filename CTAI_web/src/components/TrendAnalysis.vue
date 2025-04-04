<template>

    <div class="trend-analysis-wrapper">

        <div id="trend-analysis">
            <el-card class="box-card" style="width:250px;margin-bottom:20px;">
                <div class="clearfix">
                    <el-button type="primary" icon="el-icon-arrow-left" @click="goBack">返回诊断</el-button>
                </div>
            </el-card>

            <!-- 病人信息卡片 -->
            <el-card class="box-card" style="width:250px;height:350px">
                <div slot="header" class="clearfix">
                    <span>病人信息</span>
                </div>
                <el-descriptions :column="1">
                    <el-descriptions-item label="ID" label-class-name="my-label" content-class-name="my-content">
                        <span id="id">{{ patient['ID'] || '未知' }}</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="姓名" label-class-name="my-label" content-class-name="my-content">
                        <span id="name">{{ patient['姓名'] || '未知' }}</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="性别" label-class-name="my-label" content-class-name="my-content">
                        <span id="gender">{{ patient['性别'] || '未知' }}</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="年龄" label-class-name="my-label" content-class-name="my-content">
                        <span id="age">{{ patient['年龄'] || '未知' }}</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="电话" label-class-name="my-label" content-class-name="my-content">
                        <span id="phone">{{ patient['电话'] || '未知' }}</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="部位" label-class-name="my-label" content-class-name="my-content">
                        <span id="department">{{ patient['部位'] || '肛肠科' }}</span>
                    </el-descriptions-item>
                </el-descriptions>
            </el-card>
        </div>

        <div class="trend-content">
            <el-card style="border-radius: 8px; margin-bottom: 20px;">
                <div slot="header" class="clearfix">
                    <span><b>{{ patient['姓名'] }}</b> 患者肿瘤发展趋势分析</span>
                    <el-button style="float: right; margin-right: 10px;" type="primary" icon="el-icon-document"
                        @click="generateReport">生成分析报告</el-button>
                </div>
                <el-tabs v-model="activeTabName" type="card">
                    <el-tab-pane label="诊断记录" name="diagnosis-history">
                        <el-table :data="diagnosisHistory" style="width: 100%; max-height: 300px; overflow-y: auto;"
                            :default-sort="{ prop: 'date', order: 'descending' }">
                            <el-table-column prop="date" label="诊断日期" sortable width="150"></el-table-column>
                            <el-table-column prop="status" label="状态评估" width="120">
                                <template slot-scope="scope">
                                    <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column prop="area" label="肿瘤面积(mm²)" sortable width="150"></el-table-column>
                            <el-table-column prop="perimeter" label="肿瘤周长(mm)" sortable width="150"></el-table-column>
                            <el-table-column prop="diagnosis" label="诊断结果"></el-table-column>
                            <el-table-column label="操作" width="120">
                                <template slot-scope="scope">
                                    <el-button size="mini" type="primary"
                                        @click="viewDetail(scope.row)">查看详情</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-tab-pane>

                    <el-tab-pane label="面积变化趋势" name="area-trend">
                        <div id="area-history" style="width: 100%; height: 500px;"></div>
                    </el-tab-pane>
                    <el-tab-pane label="周长变化趋势" name="perimeter-trend">
                        <div id="perimeter-history" style="width: 100%; height: 500px;"></div>
                    </el-tab-pane>
                    <el-tab-pane label="多项指标对比" name="multi-comparison">
                        <div id="radar-chart" style="width: 100%; height: 500px;"></div>
                    </el-tab-pane>
                    <el-tab-pane label="历史图像对比" name="image-comparison">
                        <div id="image-comparison-container">
                            <p class="image-comparison-title">患者历次诊断CT图像（共 {{ historyImages.length }} 张）</p>
                            <div class="image-grid">
                                <div v-for="(imageUrl, index) in historyImages" :key="index" class="image-container">
                                    <div class="image-date">{{ diagnosisHistory[index] ? diagnosisHistory[index].date : '' }}</div>
                                    <el-image :src="imageUrl" fit="contain" class="tumor-image">
                                        <div slot="error" class="image-error">
                                            <i class="el-icon-picture-outline"></i>
                                            <p>影像加载失败</p>
                                        </div>
                                    </el-image>
                                    <div class="image-status" :class="diagnosisHistory[index] ? diagnosisHistory[index].statusType : ''">
                                        {{ diagnosisHistory[index] ? diagnosisHistory[index].status : '' }}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </el-card>

            <!-- 分析建议部分 -->
            <el-card style="border-radius: 8px;">
                <div slot="header" class="clearfix">
                    <span>DeepSeek辅助分析建议</span>
                    <el-button style="float: right" type="primary" size="small" icon="el-icon-refresh" @click="refreshAnalysis">刷新分析</el-button>
                </div>
                <div class="ai-analysis" v-loading="analysisLoading" element-loading-text="正在生成分析建议...">
                    <div v-if="analysisContent" v-html="formattedAnalysisContent" class="analysis-markdown"></div>
                    <div v-else class="analysis-placeholder">
                        <!-- 等待分析结果生成 -->
                    </div>
                </div>
            </el-card>
        </div>

        <!-- 历史记录详情对话框 -->
        <el-dialog title="诊断详情" :visible.sync="historyDetailVisible" width="60%" :before-close="handleClose">
            <div v-if="currentRecord" class="history-detail">
                <!-- 诊断日期 -->
                <div class="detail-item">
                    <span class="label">诊断日期：</span>
                    <span class="value">{{ currentRecord.date }}</span>
                </div>
                <!-- 状态评估 -->
                <div class="detail-item">
                    <span class="label">状态评估：</span>
                    <el-tag :type="currentRecord.statusType">{{ currentRecord.status }}</el-tag>
                </div>
                <!-- 肿瘤面积 -->
                <div class="detail-item">
                    <span class="label">肿瘤面积：</span>
                    <span class="value">{{ currentRecord.area }} mm²</span>
                </div>
                <!-- 肿瘤周长 -->
                <div class="detail-item">
                    <span class="label">肿瘤周长：</span>
                    <span class="value">{{ currentRecord.perimeter }} mm</span>
                </div>
                <!-- 诊断结果 -->
                <div class="detail-item">
                    <span class="label">诊断结果：</span>
                    <p class="diagnosis-text">{{ currentRecord.diagnosis }}</p>
                </div>
                <!-- 新增图片展示区块 -->
                <div class="detail-item">
                    <span class="label">肿瘤影像：</span>
                    <div class="image-container">
                        <el-image :src="currentRecord.imageUrl" :preview-src-list="[currentRecord.imageUrl]"
                            fit="contain" class="tumor-image" style="width: 100%; height: 100%;">
                            <div slot="error" class="image-error">
                                <i class="el-icon-picture-outline"></i>
                                <p>影像加载失败</p>
                            </div>
                        </el-image>
                    </div>
                </div>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="historyDetailVisible = false">关闭</el-button>
            </span>
        </el-dialog>

    </div>

</template>

<script>
import axios from 'axios';

export default {
    name: "TrendAnalysis",
    data() {
        return {
            server_url: window.location.protocol + '//' + window.location.hostname + ':5003',
            currentPatientId: '',
            patient: {
                'ID': '',
                '姓名': '',
                '性别': '',
                '年龄': '',
                '电话': '',
                '部位': ''
            },
            historyTabName: 'area-trend',
            diagnosisHistory: [], // 清空硬编码的历史记录，改为动态生成
            activeTab: 'area-trend',
            activeTabName: 'area-trend', // 默认选中面积变化趋势标签页
            historyDetailVisible: false,
            currentRecord: null,
            imageUrls: [
                '/img/tumor-1.png',
                '/img/tumor-2.png',
                '/img/tumor-3.png',
                '/img/tumor-4.png',
                '/img/tumor-5.png',
                '/img/tumor-6.png'
            ],
            // 分析建议相关数据
            analysisContent: '',      // DeepSeek API返回的分析建议内容
            analysisLoading: false,   // 加载状态
            lastAnalysisTime: null    // 上次获取分析建议的时间
        };
    },
    computed: {
        historyImages() {
            if (!this.diagnosisHistory || this.diagnosisHistory.length === 0) {
                return [];
            }
            
            const result = [];
            const recordCount = this.diagnosisHistory.length;
            
            for (let i = 0; i < recordCount; i++) {
                let randomIndex;
                if (i > 0) {
                    const lastImageIndex = this.imageUrls.indexOf(result[i-1]);
                    
                    do {
                        randomIndex = Math.floor(Math.random() * this.imageUrls.length);
                    } while (randomIndex === lastImageIndex);
                } else {
                    randomIndex = Math.floor(Math.random() * this.imageUrls.length);
                }
                
                result.push(this.imageUrls[randomIndex]);
            }
            
            return result;
        },
        // 格式化分析建议内容，处理Markdown格式
        formattedAnalysisContent() {
            // 简单的Markdown格式处理，替换标题和强调文本
            if (!this.analysisContent) return '';
            
            let content = this.analysisContent;
            
            // 替换标题
            content = content.replace(/^##\s+(.*)$/gm, '<h3>$1</h3>');
            content = content.replace(/^#\s+(.*)$/gm, '<h2>$1</h2>');
            
            // 替换加粗文本
            content = content.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
            
            // 替换换行符为HTML段落
            content = content.split('\n\n').map(paragraph => {
                // 如果段落不是以<h开头（已经被转换为HTML标签），则包装在<p>标签中
                if (!paragraph.trim().startsWith('<h') && paragraph.trim().length > 0) {
                    return `<p>${paragraph}</p>`;
                }
                return paragraph;
            }).join('\n');
            
            return content;
        }
    },
    created() {
        // 获取当前路由参数中的患者ID
        this.currentPatientId = this.$route.params.id;
        
        console.log('趋势分析组件加载:', {
            patientId: this.currentPatientId,
            path: this.$route.path
        });
        
        // 从localStorage获取当前患者信息
        const storedPatient = JSON.parse(localStorage.getItem('currentPatient'));
        if (storedPatient) {
            this.patient = {
                'ID': storedPatient.id || '',
                '姓名': storedPatient.name || '',
                '性别': storedPatient.gender || '',
                '年龄': storedPatient.age || '',
                '电话': storedPatient.phone || '',
                '部位': storedPatient.department || ''
            };
        }
        
        // 设置localStorage确保不显示欢迎弹窗
        localStorage.setItem('hideWelcomeDialog', 'true');
        
        // 加载患者历史记录
        this.loadPatientHistory();
        
        // 初始化图表
        this.$nextTick(() => {
            this.initHistoryCharts();
        });
        
        // 获取分析建议
        this.getAnalysis();
    },
    methods: {
        // 获取患者历史记录
        loadPatientHistory() {
            // 从localStorage获取所有患者历史记录
            const allHistory = JSON.parse(localStorage.getItem('patientHistoryRecords')) || {};
            
            // 检查当前患者是否有历史记录
            if (allHistory[this.currentPatientId]) {
                this.diagnosisHistory = allHistory[this.currentPatientId].records;
                console.log('已加载患者历史记录:', this.diagnosisHistory.length, '条');
            } else {
                // 检查是否为预设用户（通过ID判断）
                // 预设用户的ID格式为201900xx，而手动添加的用户ID往往大于这个范围
                const isDefaultPatient = this.currentPatientId.startsWith('2019000') || parseInt(this.currentPatientId) <= 20190015;
                
                // 如果是手动添加的患者，检查是否上传过图片
                const hasUploadedImage = localStorage.getItem(`patient_${this.currentPatientId}_hasUploaded`) === 'true';
                
                if (isDefaultPatient || hasUploadedImage) {
                    console.log('生成患者历史记录:', isDefaultPatient ? '预设用户' : '已上传图像的用户');
                    
                    // 使用上传图片后保存的数据（如果有）
                    const savedArea = parseInt(localStorage.getItem(`patient_${this.currentPatientId}_area`) || '0');
                    const savedPerimeter = parseInt(localStorage.getItem(`patient_${this.currentPatientId}_perimeter`) || '0');
                    
                    // 对于手动添加的新用户首次上传，只生成1条记录
                    // 对于预设用户，生成完整的5-7条记录
                    const forceCount = (!isDefaultPatient && hasUploadedImage) ? 1 : 0;
                    
                    this.diagnosisHistory = this.generatePatientHistory(
                        this.currentPatientId,
                        savedArea > 0 ? savedArea : 0, 
                        savedPerimeter > 0 ? savedPerimeter : 0,
                        forceCount
                    );
                } else {
                    console.log('患者尚未上传过CT图像，不显示历史记录');
                    this.diagnosisHistory = [];
                    // 提示用户
                    this.$notify({
                        title: '提示',
                        message: '此患者尚未有诊断记录，请先上传CT图像进行诊断',
                        type: 'warning',
                        duration: 5000
                    });
                    
                    // 延迟返回患者列表
                    setTimeout(() => {
                        this.$router.push('/');
                    }, 2000);
                }
            }
        },
        
        // 伪随机数生成器，基于种子生成确定性随机数
        seededRandom(seed) {
            const x = Math.sin(seed) * 10000;
            return x - Math.floor(x);
        },
        
        // 字符串哈希函数，用于生成确定性种子
        hashCode(str) {
            let hash = 0;
            for (let i = 0; i < str.length; i++) {
                const char = str.charCodeAt(i);
                hash = ((hash << 5) - hash) + char;
                hash = hash & hash; // 转换为32位整数
            }
            return Math.abs(hash);
        },
        
        // 生成患者特定的历史记录数据
        generatePatientHistory(patientId, currentArea = 0, currentPerimeter = 0, forceCount = 0) {
            // 基于患者ID创建确定性种子
            const seed = this.hashCode(patientId);
            
            // 决定历史记录条数 (对于新用户强制设为1，预设用户保持5-7条)
            const recordCount = forceCount > 0 ? forceCount : Math.floor(this.seededRandom(seed + 1) * 3) + 5;
            
            // 确定趋势变化模式 (基于患者ID，确保不同患者有不同的模式)
            // 0: 波动下降模式 - 总体下降但有明显的小幅波动
            // 1: 下降至平稳模式 - 先下降后趋于平稳
            // 2: 阶梯式波动下降 - 先波动下降再平稳再波动下降
            // 3: 缓慢波动下降 - 总体缓慢下降但波动明显
            
            // 对于预设用户（ID小于20190016），根据ID尾数均匀分配趋势模式
            // 对于非预设用户，使用随机生成的趋势模式
            let trendMode;
            if (parseInt(patientId) <= 20190015) {
                // 预设用户：根据ID尾数决定趋势模式，确保均匀分配
                const idDigit = parseInt(patientId.slice(-1));
                trendMode = idDigit % 4; // 使用尾数模4的结果作为趋势模式
            } else {
                // 非预设用户：使用随机生成的趋势模式
                trendMode = Math.floor(this.seededRandom(seed + 100) * 4);
            }
            
            console.log('患者趋势模式:', ['波动下降', '下降至平稳', '阶梯式波动下降', '缓慢波动下降'][trendMode]);
            
            // 生成历史记录数组
            const records = [];
            
            // 如果有当前上传的图像数据，将其用作最新记录的基础
            let baseArea = currentArea > 0 ? currentArea : 1000 + Math.floor(this.seededRandom(seed + 2) * 400);
            let basePerimeter = currentPerimeter > 0 ? currentPerimeter : 150 + Math.floor(this.seededRandom(seed + 3) * 150);
            
            // 当前日期作为最新记录的日期
            const today = new Date();
            
            // 创建历史记录，从最新到最早
            for (let i = 0; i < recordCount; i++) {
                // 计算记录日期（每条记录间隔15天）
                const recordDate = new Date(today);
                recordDate.setDate(recordDate.getDate() - (i * 15));
                
                // 格式化日期为 YYYY-MM-DD
                const dateString = `${recordDate.getFullYear()}-${String(recordDate.getMonth() + 1).padStart(2, '0')}-${String(recordDate.getDate()).padStart(2, '0')}`;
                
                // 第一条记录使用基准值或实际上传值
                let area, perimeter;
                
                if (i === 0) {
                    area = Math.round(baseArea);
                    perimeter = Math.round(basePerimeter);
                } else {
                    // 为每个点计算增长因子和波动值
                    let increaseFactor;
                    
                    // 基础波动因子，使曲线不平滑，但保持总体下降趋势
                    // 注意：波动因子只对最终结果做微调
                    // 范围在0.98-1.03之间，表示相邻两点之间有+/-2%的波动
                    const waveFluctuation = 0.98 + (this.seededRandom(seed + i * 37 + 5) * 0.05);
                    
                    switch(trendMode) {
                        case 0: // 波动下降模式 - 总体下降但有明显的小幅波动
                            // 基本增长因子为1.07-1.13
                            increaseFactor = 1.07 + (this.seededRandom(seed + i + 20) * 0.06);
                            
                            // 增加随机波动
                            if (this.seededRandom(seed + i * 13) < 0.3) {
                                // 30%概率有较大波动
                                increaseFactor *= (1 + (this.seededRandom(seed + i * 7) - 0.5) * 0.1);
                            }
                            break;
                            
                        case 1: // 下降至平稳模式 - 先下降后趋于平稳
                            if (i < recordCount * 0.6) {
                                // 前60%记录有较大下降
                                increaseFactor = 1.08 + (this.seededRandom(seed + i + 20) * 0.1);
                            } else {
                                // 后40%记录趋于平稳
                                // 确保平稳期仍有小波动但基本稳定，增长因子接近1
                                increaseFactor = 1.005 + (this.seededRandom(seed + i + 20) * 0.015);
                            }
                            break;
                            
                        case 2: // 阶梯式波动下降 - 先波动下降再平稳再波动下降
                            if (i < recordCount * 0.3) {
                                // 前30%记录波动下降
                                increaseFactor = 1.1 + (this.seededRandom(seed + i + 20) * 0.08);
                                // 增加波动
                                increaseFactor *= (1 + (this.seededRandom(seed + i * 11) - 0.5) * 0.1);
                            } else if (i < recordCount * 0.6) {
                                // 中间30%记录平稳
                                increaseFactor = 1.01 + (this.seededRandom(seed + i + 20) * 0.02);
                            } else {
                                // 后40%记录再次波动下降
                                increaseFactor = 1.08 + (this.seededRandom(seed + i + 20) * 0.07);
                                // 增加波动
                                increaseFactor *= (1 + (this.seededRandom(seed + i * 17) - 0.5) * 0.1);
                            }
                            break;
                            
                        case 3: // 缓慢波动下降 - 总体缓慢下降但波动明显
                            // 基本增长因子较小，但波动较大
                            increaseFactor = 1.03 + (this.seededRandom(seed + i + 20) * 0.04);
                            
                            // 添加显著波动
                            increaseFactor *= (1 + (this.seededRandom(seed + i * 23) - 0.5) * 0.15);
                            
                            // 确保增长因子不低于1，避免上升趋势
                            increaseFactor = Math.max(1.005, increaseFactor);
                            break;
                            
                        default:
                            increaseFactor = 1.08 + (this.seededRandom(seed + i + 20) * 0.06);
                            break;
                    }
                    
                    // 每一步都增加小波动，让曲线更自然
                    // 应用波动因子到增长因子
                    increaseFactor *= waveFluctuation;
                    
                    // 确保增长因子不小于1.001，防止曲线上升
                    increaseFactor = Math.max(1.001, increaseFactor);
                    
                    // 后续记录递增（向过去增加，表示病情在好转）
                    area = Math.round(records[i-1].area * increaseFactor);
                    perimeter = Math.round(records[i-1].perimeter * (increaseFactor * 0.97 + 0.03));
                }
                
                // 根据记录序号确定状态
                let status, statusType;
                if (i === 0) {
                    status = '好转';
                    statusType = 'success';
                } else if (i === recordCount - 1) {
                    status = '初诊';
                    statusType = 'info';
                } else if (i < recordCount / 3) {
                    status = '好转';
                    statusType = 'success';
                } else if (i < recordCount * 2 / 3) {
                    status = '稳定';
                    statusType = 'warning';
                } else {
                    status = '恶化';
                    statusType = 'danger';
                }
                
                // 生成诊断评估
                const diagnosis = this.generateDiagnosis(status, i, recordCount);
                
                // 添加记录
                records.push({
                    id: i + 1,
                    date: dateString,
                    status,
                    statusType,
                    area,
                    perimeter,
                    diagnosis,
                    // 为每条记录添加图像URL，使用imageUrls数组循环分配
                    imageUrl: this.imageUrls[i % this.imageUrls.length]
                });
            }
            
            // 保存生成的历史记录
            this.savePatientHistory(patientId, records);
            
            return records;
        },
        
        // 生成诊断评估文本
        generateDiagnosis(status, index, totalRecords) {
            // 诊断模板池
            const diagnosisTemplates = {
                '好转': [
                    '肿瘤区域明显缩小，治疗反应良好，建议继续现有治疗方案。',
                    '肿瘤体积持续减小，患者对治疗反应积极，预后良好。',
                    '肿瘤边界更加规则，密度降低，说明坏死组织正在被吸收。',
                    '治疗效果显著，肿瘤活性区域明显减少，继续当前方案。'
                ],
                '稳定': [
                    '肿瘤区域基本稳定，未见明显变化，需继续密切监测。',
                    '肿瘤大小变化不明显，建议维持现有治疗并定期复查。',
                    '肿瘤形态略有变化但体积稳定，治疗反应一般。',
                    '病灶边界略微模糊，可能表明炎症反应，但总体稳定。'
                ],
                '恶化': [
                    '肿瘤区域略有增大，需评估调整当前治疗方案。',
                    '肿瘤密度增加，边界不规则，考虑肿瘤活性增强。',
                    '与上次相比肿瘤侵犯范围扩大，建议更换治疗方案。',
                    '病灶形态变化明显，可能表明治疗效果不佳。'
                ],
                '初诊': [
                    '初次诊断，肿瘤区域较大，建议立即开始治疗。',
                    '首次检查发现明显异常，需进一步检查确认病理类型。',
                    '初步诊断为恶性肿瘤，边界不规则，密度不均匀。',
                    '新发现病灶，大小约为{area}mm²，需立即采取治疗措施。'
                ]
            };
            
            // 使用患者ID和索引生成伪随机数，选择诊断模板
            const randomIndex = Math.floor(this.seededRandom((this.hashCode(this.currentPatientId) + index) * 100) * diagnosisTemplates[status].length);
            let diagnosis = diagnosisTemplates[status][randomIndex];
            
            // 替换模板中的占位符 - 修复可选链操作符问题
            if (index === totalRecords - 1 && diagnosis.includes('{area}')) {
                let areaValue = '未知';
                if (this.diagnosisHistory && this.diagnosisHistory[index] && this.diagnosisHistory[index].area) {
                    areaValue = this.diagnosisHistory[index].area;
                }
                diagnosis = diagnosis.replace('{area}', areaValue);
            }
            
            return diagnosis;
        },
        
        // 保存患者历史记录
        savePatientHistory(patientId, records) {
            // 获取现有历史记录数据
            const allHistory = JSON.parse(localStorage.getItem('patientHistoryRecords')) || {};
            
            // 更新当前患者的记录
            allHistory[patientId] = {
                lastUpdate: new Date().toISOString(),
                records: records
            };
            
            // 保存回localStorage
            localStorage.setItem('patientHistoryRecords', JSON.stringify(allHistory));
            console.log('已保存患者历史记录:', patientId, records.length, '条');
        },
        goBack() {
            // 返回诊断页面
            this.$router.push(`/patient/${this.currentPatientId}`);
        },
        handleClose(done) {
            this.$confirm("确认关闭？")
                .then(_ => {
                    done();
                })
                .catch(_ => { });
        },
        // 获取随机肿瘤图片的方法
        getRandomTumorImage() {
            // 随机选择imageUrls数组中的一个元素
            const randomIndex = Math.floor(Math.random() * this.imageUrls.length);
            return this.imageUrls[randomIndex];
        },
        viewDetail(record) {
            // 为当前记录设置一个随机图片URL
            const recordWithImage = { ...record, imageUrl: this.getRandomTumorImage() };
            this.currentRecord = recordWithImage;
            this.historyDetailVisible = true;
        },
        generateReport() {
            this.$message({
                message: '分析报告已生成，正在下载...',
                type: 'success'
            });

            // 模拟下载延迟
            setTimeout(() => {
                this.$notify({
                    title: '下载完成',
                    message: '肿瘤发展趋势分析报告已保存至您的下载文件夹',
                    type: 'success',
                    duration: 3000
                });
            }, 1500);
        },
        initHistoryCharts() {
            // 如果没有历史记录，不初始化图表
            if (!this.diagnosisHistory || this.diagnosisHistory.length === 0) {
                console.log('没有历史记录数据，不初始化图表');
                return;
            }
            
            // 增加延迟时间到500ms，确保DOM已完全渲染
            setTimeout(() => {
                console.log('开始渲染图表');
                try {
                    // 提取数据
                    const dates = this.diagnosisHistory.map(record => record.date).reverse();
                    const areas = this.diagnosisHistory.map(record => record.area).reverse();
                    const perimeters = this.diagnosisHistory.map(record => record.perimeter).reverse();
                    
                    console.log('图表数据:', { dates, areas, perimeters });
                    
                    // 初始化面积趋势图
                    const areaChart = this.$echarts.init(document.getElementById('area-history'));
                    areaChart.setOption({
                        backgroundColor: '#ffffff',
                        title: {
                            text: '肿瘤面积变化趋势',
                            subtext: '单位: mm²',
                            left: 'center',
                            top: 10
                        },
                        tooltip: {
                            trigger: 'axis',
                            formatter: '{b}<br />面积: {c} mm²'
                        },
                        grid: {
                            left: 60,  // 使用固定像素值
                            right: 60,
                            bottom: 80,
                            top: 80,
                            containLabel: true
                        },
                        xAxis: {
                            type: 'category',
                            data: dates,
                            name: '诊断日期',
                            nameLocation: 'middle',
                            nameGap: 40,
                            axisLabel: {
                                rotate: 45,
                                margin: 20
                            }
                        },
                        yAxis: {
                            type: 'value',
                            name: '面积 (mm²)',
                            nameGap: 35,
                            min: function(value) {
                                return Math.floor(value.min * 0.9);
                            }
                        },
                        series: [{
                            name: '肿瘤面积',
                            type: 'line',
                            symbolSize: 8,  // 增大数据点
                            data: areas,
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                            markLine: {
                                data: [
                                    {type: 'average', name: '平均值'}
                                ]
                            },
                            lineStyle: {
                                width: 3,
                                color: '#17b3a3'
                            },
                            areaStyle: {
                                color: {
                                    type: 'linear',
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [{
                                        offset: 0, color: 'rgba(23, 179, 163, 0.5)'
                                    }, {
                                        offset: 1, color: 'rgba(23, 179, 163, 0.1)'
                                    }]
                                }
                            }
                        }]
                    });
                    
                    console.log('面积图表渲染完成');
                    
                    // 初始化周长趋势图
                    const perimeterChart = this.$echarts.init(document.getElementById('perimeter-history'));
                    perimeterChart.setOption({
                        backgroundColor: '#ffffff',
                        title: {
                            text: '肿瘤周长变化趋势',
                            subtext: '单位: mm',
                            left: 'center',
                            top: 10
                        },
                        tooltip: {
                            trigger: 'axis',
                            formatter: '{b}<br />周长: {c} mm'
                        },
                        grid: {
                            left: 60,  // 使用固定像素值
                            right: 60,
                            bottom: 80,
                            top: 80,
                            containLabel: true
                        },
                        xAxis: {
                            type: 'category',
                            data: dates,
                            name: '诊断日期',
                            nameLocation: 'middle',
                            nameGap: 40,
                            axisLabel: {
                                rotate: 45,
                                margin: 20
                            }
                        },
                        yAxis: {
                            type: 'value',
                            name: '周长 (mm)',
                            nameGap: 35,
                            min: function(value) {
                                return Math.floor(value.min * 0.9);
                            }
                        },
                        series: [{
                            name: '肿瘤周长',
                            type: 'line',
                            symbolSize: 8,  // 增大数据点
                            data: perimeters,
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                            markLine: {
                                data: [
                                    {type: 'average', name: '平均值'}
                                ]
                            },
                            lineStyle: {
                                width: 3,
                                color: '#409EFF'
                            },
                            areaStyle: {
                                color: {
                                    type: 'linear',
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [{
                                        offset: 0, color: 'rgba(64, 158, 255, 0.5)'
                                    }, {
                                        offset: 1, color: 'rgba(64, 158, 255, 0.1)'
                                    }]
                                }
                            }
                        }]
                    });
                    
                    console.log('周长图表渲染完成');
                    
                    // 初始化雷达图
                    const radarChart = this.$echarts.init(document.getElementById('radar-chart'));
                    
                    // 准备数据：最新的和最早的记录进行对比
                    const latestRecord = this.diagnosisHistory[0];
                    const earliestRecord = this.diagnosisHistory[this.diagnosisHistory.length - 1];
                    
                    radarChart.setOption({
                        backgroundColor: '#ffffff',
                        title: {
                            text: '肿瘤指标对比分析',
                            left: 'center',
                            top: 10
                        },
                        tooltip: {
                            trigger: 'item'
                        },
                        legend: {
                            data: ['初诊', '最近诊断'],
                            bottom: 10
                        },
                        radar: {
                            center: ['50%', '55%'],  // 居中并稍微向下调整
                            radius: '60%',          // 控制雷达图大小
                            shape: 'circle',
                            indicator: [
                                { name: '面积', max: Math.max(...areas) + 50 },
                                { name: '周长', max: Math.max(...perimeters) + 20 },
                                { name: '灰度均值', max: 130 },
                                { name: '似圆度', max: 0.9 },
                                { name: '灰度方差', max: 50 }
                            ]
                        },
                        series: [{
                            name: '初诊 vs 最近',
                            type: 'radar',
                            data: [
                                {
                                    value: [earliestRecord.area, earliestRecord.perimeter, 115, 0.65, 35],
                                    name: '初诊',
                                    symbolSize: 6,
                                    lineStyle: {
                                        width: 2,
                                        color: '#E6A23C'
                                    },
                                    areaStyle: {
                                        color: 'rgba(230, 162, 60, 0.3)'
                                    }
                                },
                                {
                                    value: [latestRecord.area, latestRecord.perimeter, 95, 0.82, 26],
                                    name: '最近诊断',
                                    symbolSize: 6,
                                    lineStyle: {
                                        width: 2,
                                        color: '#67C23A'
                                    },
                                    areaStyle: {
                                        color: 'rgba(103, 194, 58, 0.3)'
                                    }
                                }
                            ]
                        }]
                    });
                    
                    console.log('雷达图渲染完成');
                    
                    // 窗口调整时重新计算图表大小
                    window.addEventListener('resize', () => {
                        console.log('窗口大小变化，重新调整图表大小');
                        areaChart.resize();
                        perimeterChart.resize();
                        radarChart.resize();
                    });
                    
                    // 为每个标签页添加点击事件，确保激活时重新渲染图表
                    this.$watch('activeTabName', (newVal) => {
                        console.log('标签页切换到:', newVal);
                        this.$nextTick(() => {
                            if (newVal === 'area-trend') {
                                areaChart.resize();
                            } else if (newVal === 'perimeter-trend') {
                                perimeterChart.resize();
                            } else if (newVal === 'multi-comparison') {
                                radarChart.resize();
                            }
                        });
                    });
                } catch (error) {
                    console.error('图表渲染失败:', error);
                }
            }, 500); // 增加延迟到500ms
        },
        format(percentage) {
            return percentage + '%';
        },
        // 获取AI辅助分析建议
        getAnalysis() {
            // 如果距离上次请求不足1分钟，则不重新请求
            if (this.lastAnalysisTime && (Date.now() - this.lastAnalysisTime) < 60000) {
                console.log('距离上次请求不足1分钟，使用缓存数据');
                return;
            }
            
            this.analysisLoading = true;
            
            axios.get(`${this.server_url}/api/analysis`)
                .then(response => {
                    if (response.data.status === 1) {
                        this.analysisContent = response.data.data;
                        this.lastAnalysisTime = Date.now();
                        console.log('成功获取分析建议');
                    } else {
                        console.error('获取分析建议失败:', response.data.message);
                        this.$message.error('获取分析建议失败，请稍后重试');
                    }
                })
                .catch(error => {
                    console.error('请求分析建议出错:', error);
                    this.$message.error('网络错误，无法获取分析建议');
                })
                .finally(() => {
                    this.analysisLoading = false;
                });
        },
        
        // 刷新分析建议
        refreshAnalysis() {
            // 强制刷新分析建议
            this.lastAnalysisTime = null;
            this.getAnalysis();
        }
    }
};
</script>

<style scoped>
.trend-analysis-wrapper {
    display: flex;
    margin: 20px;
    gap: 20px;
}

.trend-content {
    flex: 1;
    min-width: 0;
}

/* 分析项目样式 */
.ai-analysis {
    margin-top: 15px;
}

.analysis-item {
    margin-bottom: 15px;
    border-bottom: 1px dashed #eee;
    padding-bottom: 15px;
}

.analysis-item:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

.analysis-item h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 16px;
    color: #333;
}

.trend-good {
    color: #67c23a;
    font-weight: bold;
}

.trend-warning {
    color: #e6a23c;
    font-weight: bold;
}

.trend-danger {
    color: #f56c6c;
    font-weight: bold;
}

.percentage, .date-recommend {
    font-weight: bold;
    color: #409eff;
}

.risk-level {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.risk-text {
    margin-top: 10px;
    font-weight: bold;
    color: #67c23a;
}

/* 诊断详情对话框样式 */
.history-detail {
    max-height: 70vh;
    overflow-y: auto;
    padding: 15px;
}

.detail-item {
    margin-bottom: 15px;
}

.detail-item .label {
    font-weight: bold;
    margin-right: 10px;
}

.diagnosis-text {
    line-height: 1.6;
    margin-top: 5px;
}

.image-container {
    margin-top: 10px;
    text-align: center;
    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}

.tumor-image {
    max-width: 100%;
    max-height: 380px;
    border: 1px solid #eee;
    border-radius: 4px;
    object-fit: contain;
}

.image-error {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 380px;
    color: #909399;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.image-error i {
    font-size: 32px;
    margin-bottom: 10px;
}

/* 图像对比容器样式 */
#image-comparison-container {
    width: 100%;
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
}

.image-comparison-title {
    font-weight: bold;
    margin-bottom: 15px;
    font-size: 16px;
    color: #409EFF;
}

.image-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: flex-start;
}

.image-container {
    flex: 0 0 calc(25% - 15px);  /* 每行4张图片，减去间距 */
    margin-bottom: 20px;
    border: 1px solid #ebeef5;
    border-radius: 6px;
    padding: 10px;
    transition: all 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.image-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.image-date {
    font-weight: bold;
    margin-bottom: 8px;
    text-align: center;
    font-size: 14px;
    color: #606266;
}

.tumor-image {
    width: 100%;
    height: 180px;
    object-fit: contain;
    margin-bottom: 8px;
    background-color: #f8f8f8;
}

.image-status {
    font-weight: bold;
    padding: 2px 0;
    border-radius: 4px;
    text-align: center;
    font-size: 13px;
}

.success {
    background-color: #f0f9eb;
    border: 1px solid #e1f3d8;
    color: #67c23a;
}

.warning {
    background-color: #fdf6ec;
    border: 1px solid #faecd8;
    color: #e6a23c;
}

.danger {
    background-color: #fef0f0;
    border: 1px solid #fde2e2;
    color: #f56c6c;
}

.info {
    background-color: #f4f4f5;
    border: 1px solid #e9e9eb;
    color: #909399;
}

.image-error {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 180px;
    color: #909399;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.image-error i {
    font-size: 32px;
    margin-bottom: 10px;
}

/* 适配不同屏幕尺寸 */
@media screen and (max-width: 1400px) {
    .image-container {
        flex: 0 0 calc(33.333% - 15px);  /* 每行3张图片 */
    }
}

@media screen and (max-width: 1100px) {
    .image-container {
        flex: 0 0 calc(50% - 15px);  /* 每行2张图片 */
    }
}

@media screen and (max-width: 768px) {
    .image-container {
        flex: 0 0 100%;  /* 每行1张图片 */
    }
}

/* 表格滚动样式 */
.el-table {
    max-height: 300px !important;
    overflow-y: auto !important;
}

/* 文字标签样式 */
.my-label {
    font-weight: bold;
    color: #606266;
}

.my-content {
    font-size: 14px;
}

/* 添加分析建议相关样式 */
.analysis-markdown {
    padding: 0 15px;
}

.analysis-markdown h2 {
    font-size: 18px;
    color: #409EFF;
    margin-top: 20px;
    margin-bottom: 15px;
    border-bottom: 1px solid #EBEEF5;
    padding-bottom: 8px;
}

.analysis-markdown h3 {
    font-size: 16px;
    color: #303133;
    margin-top: 15px;
    margin-bottom: 10px;
}

.analysis-markdown p {
    line-height: 1.6;
    margin-bottom: 10px;
    color: #606266;
}

.analysis-markdown strong {
    color: #409EFF;
    font-weight: bold;
}

.analysis-placeholder {
    padding: 0 15px;
}
</style>
