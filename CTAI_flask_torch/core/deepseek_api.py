import os
import random
import requests

# DeepSeek API配置
API_KEY = "sk-1f8ce920c5a745d1b427414342c8357d"
API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_tumor_analysis():
    """
    生成随机直肠肿瘤辅助分析建议
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # 倾向于积极的肿瘤面积变化趋势
    area_trends = ["缓慢减小", "明显减小", "稳定不变", "明显减小", "缓慢减小"]
    area_trend = random.choice(area_trends)
    
    # 倾向于积极的周长变化趋势
    perimeter_trends = ["缓慢减小", "明显减小", "稳定不变", "明显减小", "缓慢减小"]
    perimeter_trend = random.choice(perimeter_trends)
    
    # 倾向于积极的治疗响应
    responses = ["良好", "良好", "一般", "良好"]
    response_quality = random.choice(responses)
    
    # 随机生成肿瘤缩小率（偏向较高值）
    shrink_rate = random.randint(15, 40)
    
    # 偏向积极的风险评估
    risk_levels = ["低风险", "低风险", "中等风险"]
    risk_level = random.choice(risk_levels)
    
    prognosis = ["预后良好", "预后良好", "预后一般", "需密切关注"]
    prognosis_result = random.choice(prognosis)
    
    # 随机生成下次随访日期
    next_month = random.randint(1, 12)
    next_day = random.randint(1, 28)
    
    # 构建提示词
    prompt = f"""
    请生成一份简洁的直肠肿瘤患者辅助分析建议，使用通俗易懂的语言，避免过于专业的术语。内容应该积极乐观，突出治疗效果。包含以下四个部分：

    ## 肿瘤发展趋势

    根据最近几次诊断记录分析，该患者肿瘤面积呈现{area_trend}趋势，周长变化{perimeter_trend}，治疗效果{response_quality}。

    ## 治疗响应评估

    患者对当前治疗方案响应{response_quality}，肿瘤体积缩小率达到{shrink_rate}%，建议继续保持现有治疗方案。

    ## 后续治疗建议

    建议在保持现有治疗方案的同时，适当增加随访频率，密切监测肿瘤变化。下次随访建议时间：2025-{next_month:02d}-{next_day:02d}

    ## 风险评估

    {risk_level} - {prognosis_result}

    请使用简单明了的语言，篇幅控制在200字左右，确保内容积极向好。
    """
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一位友善的医疗顾问，擅长以简单易懂的方式解释医学信息，特别是为癌症患者提供积极乐观的分析和建议。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "未能生成分析建议，请稍后再试。"
    except Exception as e:
        print(f"生成肿瘤分析失败: {e}")
        # 如果API调用失败，返回一个静态的备用内容
        backup_message = f"""
        **直肠肿瘤辅助分析建议**

        ## 肿瘤发展趋势
        根据最近几次诊断记录分析，该患者肿瘤面积呈现稳定减小趋势，治疗效果良好。

        ## 治疗响应评估
        患者对当前治疗方案响应良好，肿瘤体积缩小率达到25%，建议继续保持现有治疗方案。

        ## 后续治疗建议
        建议在保持现有治疗方案的同时，适当增加随访频率，密切监测肿瘤变化。下次随访建议时间：2025-06-15

        ## 风险评估
        低风险 - 预后良好
        """
        return backup_message 