import streamlit as st
import requests
import json
#百度云OCR API的访问地址
def get_access_token(api_key,secret_key):

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(api_key,secret_key)
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def main(prompt,api_key,secret_key):
    '''
    url=https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/vt99f5saztcj7z75/
    '''
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/vt99f5saztcj7z75/?access_token=" + get_access_token(api_key,secret_key)
    
    payload = json.dumps({
        "query": prompt,
        "plugins":["uuid-zhishiku"],
        "verbose":False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response.text
    


if __name__ == '__main__':
    st.sidebar.header('❤️‍🔥欢迎关注')
    st.sidebar.image('media_code.jpg',width=200)
    
    st.sidebar.header('💡问答提示')
    st.sidebar.subheader('📫问URL')
    st.sidebar.write('通过询问注释数据库、分析工具和测序数据库的URL，例如，请以表格的形式提供3条miRNA相关的URL及其简要介绍。\n 使用语言模型进行检索的好处是可以进行形式上的整理，不局限语言，缺点是返回的结果不够丰富。')
    # st.sidebar.divider()
    # st.sidebar.subheader('🩺问疾病')
    # st.sidebar.write('直接输入疾病的名称，可以进行较综合的答案。')
    # st.sidebar.divider()
    # st.sidebar.subheader('📚机器学习知识类')
    # st.sidebar.write('知识库内收录了一些独特的经验和体会，包括：医学预测模型矩阵计划？DCA分析的注意事项？预测模型+临床检查的筛查策略？局部评价介绍？XXAPP简介？医学预测模型APP制作规范？')
    st.sidebar.divider()
    st.sidebar.header('⚙️推广合作')
    st.sidebar.write("可以就技术和科研问题展开合作。问答机器人导航使用百度千帆大模型中自建知识库；python语言APP使用steamlit构建；R语言APP使用shiny构建；临床预测模型使用R或python语言构建") 
    
    st.title("📱医学生物信息学URLs") 
    st.write('''
                收录的生物信息学的网络资源可以分为三类：\n
                1.测序数据库，存储了原始的二代测序或者基因芯片获得的基因数据，如TCGA；\n
                2.注释数据库，存储了归类的基因数据，特别是研究证实的属于某类细胞、某条信号通路的基因数据，比如免疫浸润相关基因等；\n
                3.网络分析工具，用于分析生物信息的各种工具，比如基因序列比对的工具。
                
                ''')
    st.subheader('📜最流行的数据库和工具')
    with st.expander('🗃️注释数据库 🧬测序数据库 🛠️分析工具 ',expanded=True):
        col1,col2,col3=st.columns(3)
        with col1:
            st.write("🗃️注释数据库")
            st.write("🗃️注释数据库")
            st.write('🗃️注释数据库')
        with col2:
            st.write("🗃️注释数据库")
            st.write('🗃️注释数据库')
        with col3:
            st.write("🗃️注释数据库")
            st.write('🗃️注释数据库')
    
    #导航机器人
    st.subheader('🤖导航机器人')
    api_key=st.secrets["API_key"]
    secret_key=st.secrets["secret_key"]
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "你好！我收藏我很多的生物信息学的URL，欢迎询问！"}]
    # for msg in st.session_state["messages"]:
    #     st.chat_message(msg["role"]).write(msg["content"])  
    #
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the prior chat messages
    # print(st.session_state.messages)    
    for message in st.session_state.messages: 
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = main(prompt,api_key,secret_key)
                msg = json.loads(response)
                answer = msg["result"]
                st.session_state.messages.append({'role':'assistant','content':answer})#后台necessary，role 和content
                st.write(answer)

     