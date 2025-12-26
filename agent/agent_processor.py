from . import proposal_template as pt
from ollamaLLM import send_messages_to_LLM

messages = [{
    "role": "system",
    "content": pt.system_role
}
#,{
#     "role": "user",
#     "content": """
#     我想要做一個能夠改善商業競賽的agent，
#     讓參加競賽的使用者能夠完善他們的競賽，
#     能夠幫助他們釐清提案邏輯
#     並整理提案架構
#                           """
# },{
#     "role": "assistant"
#     "content":"""
# 總分100分，你拿到13分
# 現況與問題：7
# 解決方案構想：6
# 市場規模與趨勢：0
# 競爭者分析：0
# 商業模式：0

# 建議方向：
# 1. 現況與問題：說明痛點會怎樣影響參賽者（如提案失敗率、時間成本）。
# 2. 解決方案：具體描述 agent 如何運作（例如 AI 分析、模板生成、即時回饋），並說明有何創新點與現有工 具差別。
# 3. 市場規模：列出目標使用者數量、相關產業的市場規模（如商業競賽平台、創業加速器），提供資料來源或合理推估依據，說明成長趨勢。
# 4. 競爭者分析：列舉目前市場上類似的提案輔助工具，分析其優缺點，說明你的方案在功能、成本或使用者體驗上如何差異化，並指出尚未被滿足的需求。
# 5. 商業模式：說明收入來源（訂閱、付費升級、企業授權等），主要成本（開發、雲端運算、行銷），以及價值如何透過平台、API 或合作夥伴傳遞給客戶。


# 感謝您提供的提案。依照五大評分構面，您的總分只有 13 分，主要因為缺少對痛點影響的說明、具體的執行方 法、任何市場或競爭資訊，以及完整的商業模式描述。上面列出的 missing_points 與 improvement_suggestions 可協助您逐項補強，讓提案更完整、說服力更強。祝您修正順利！
# """
# }
]



def  send_message_to_agent(user_name: str, user_message: str, mode: int) -> str:
    """
    使用者傳入提案內容，並選擇想要的模式，根據所選的模式進行處理後，傳LLM回覆的訊息

    參數:
        user_name: 使用者名字
        user_message: 使用者傳的訊息
        mode (int):
            1: 輸入競賽名稱
            2: 討論提案
            3: LLM 整理提案
            4: 輸入提案內容
    回傳:
        str: LLM回覆的訊息
    """
    if mode == 1:
        #clear_user_message_history(user_name)
        #get_user_message_history(user_name: str, role: str) -> str(user_message_history):
        print(f"找到{user_message}競賽")
        result_message = f"{user_message}" + pt.completion_info
        messages.append({"role" : "user", "content": result_message})
        print(send_messages_to_LLM(messages))
    elif mode == 2:
        #get_user_message_history(user_name: str, role: str) -> str(user_message_history):
        result_message = f"{user_message}" + pt.discussion
        messages.append({"role" : "user", "content": result_message})
        LLM_response = discuss_proposal(messages)
        print(LLM_response)
        #set_user_message_history(user_name: str, role: str, message: str):
    elif mode == 3:
        #implement get_user_message_history(user_name: str, role: str) -> str(user_message_history):
        # 新增模板
        # 傳給LLM
        # 接收LLM結果
        # 在database 紀錄
        print("LLM回傳整理的提案")
        result_message = "LLM回傳整理的提案"
    elif mode == 4:
        #implement get_user_message_history(user_name: str, role: str) -> str(user_message_history):
        # 新增模板
        # 傳給LLM
        # 接收LLM結果
        # 在database 紀錄
        result_message = pt.sysetm_promt + pt.proposal_reply_format + f"{user_message}"
        messages.append({"role" : "user", "content": result_message})
        LLM_response = score_proposal(messages)
        print(LLM_response)

    return result_message

def discuss_proposal(messages: list[dict[str,str]]) -> str:
    response = send_messages_to_LLM(messages)
    return response["reply_to_user"]

def score_proposal(messages: list[dict[str,str]]) -> str:
    response = send_messages_to_LLM(messages)
    response_processed = f"""總分100分，你拿到{response["scores"]["total_score"]}分
現況與問題：{response["scores"]["problem_analysis"]}
解決方案構想：{response["scores"]["solution_design"]}
市場規模與趨勢：{response["scores"]["market_analysis"]}
競爭者分析：{response["scores"]["business_model"]}
商業模式：{response["scores"]["competitor_analysis"]}

建議方向：
{response["improvement_suggestions"]["detailed_version"]}


{response["reply_to_user"]}
    """
    return response_processed