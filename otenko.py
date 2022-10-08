import vrmapi

##################################################################
#
#　ユーザー様へ
#
#　リソースの選択番号を増やした言時は、67行目の一番最後の「20」の部分を希望の数字に変更して上書き保存するだけです。
#
##################################################################

# ファイル読み込みログ表示
vrmapi.LOG("お天候くん開始！　Version.1.1")

LAYOUT = vrmapi.LAYOUT()
IMGUI = vrmapi.ImGui()

skyfactor = [0.0]
skyload_res = [0]
skyImgChkMax = 50 # ★天球スライダー最大値(init処理内で更新)
skyImgList = []   # ★天球スライダー用リソースリスト(ID配列)
weathertype = [0]
weatherdict = {0:'晴れ', 1:'雨', 2:'雪'}
suntype = [0]
sundict = {0:'昼間', 1:'朝日', 2:'夕日', 3:'夜間', 4:'曇り', 5:'夕暮れ', 6:'夕日2'}
fogtype = [0]
fogdict = {0:'標準', 1:'都市', 2:'山岳', 3:'朝霧', 4:'濃霧', 5:'郊外'}
fog_amount = 1.0
fog_amount_list = [1.0]
sun_pos = [[0], [45]] # 太陽位置(緯度,経度)
_guidisp = True       # TrueでGUI操作盤を表示

def vrmevent(obj,ev,param):
    global _guidisp
    if ev == 'init':
        init(obj)
    elif ev == 'broadcast':
        dummy = 1
    elif ev == 'timer':
        dummy = 1
    elif ev == 'time':
        dummy = 1
    elif ev == 'after':
        dummy = 1
    elif ev == 'frame':
        if _guidisp:
            gui_otenkokun()
    elif ev == 'keydown':
        if param['keycode'] == 'P':
            # GUI表示をON/OFF
            _guidisp = (_guidisp+1)%2
        return

# ★初期化処理
def init(obj):
    obj.SetEventFrame()
    obj.SetEventKeyDown('P')

    # リソース探索
    global skyImgChkMax
    global skyImgList
    for res_id in range(1, skyImgChkMax):
        res_type = obj.GetResourceType(res_id)
        # PNGのとき
        if res_type == 3:
            skyImgList.append(res_id)
            vrmapi.LOG("リソース[" + str(res_id) + "] を天球スライダー番号 " + str(len(skyImgList)) + " に読み込み")
        else:
            vrmapi.LOG("リソース[" + str(res_id) + "] を確認。タイプ：" + str(res_type))
    # スライダー幅を最適化
    skyImgChkMax = len(skyImgList)

def gui_otenkokun():
    global LAYOUT
    global skyfactor
    global skyload_res
    global skyImgList
    global weathertype
    global suntype
    global fogtype
    global fog_amount
    global fog_amount_list

    IMGUI.Begin('otenkokun_window', 'お天候くん')
    IMGUI.Text("背景テクスチャー欄で設定した天空0と天空1の合成率")  
    if IMGUI.SliderFloat('skyfactorslider', '合成率', skyfactor, 0.0, 1.0):
        LAYOUT.SKY().SetSkyFactor(skyfactor[0]) 
    IMGUI.Separator() 
    IMGUI.Text("天空0を変更")
    # 天球リストからリソースIDを呼び出し
    if IMGUI.SliderInt('skyload_res_slider', 'リソース番号', skyload_res, 1, skyImgChkMax):
        # リスト配列0開始とスライダー1開始のズレに注意
        LAYOUT.SKY().LoadSkyImage(0, skyImgList[skyload_res[0] - 1])
    IMGUI.Text("天空0をリセット")
    if IMGUI.Button("b1", "リセット"):
        LAYOUT.SKY().ResetSkyImage(0)
    IMGUI.Separator()
    IMGUI.Text("天気")
    for key, name in weatherdict.items():
        IMGUI.SameLine()
        if IMGUI.RadioButton('btnweather{}'.format(key), name, weathertype, key):
            LAYOUT.SKY().SetWeather(key)
    IMGUI.Separator()
    IMGUI.Text("太陽光")
    for key, name in sundict.items():
        IMGUI.SameLine()
        if IMGUI.RadioButton('btnsun{}'.format(key), name, suntype, key):
            LAYOUT.SKY().SetSunType(key, 1)
    IMGUI.Separator()
    IMGUI.Text("太陽の位置")
    if IMGUI.SliderFloat('sun_longitude2', '経度', sun_pos[0], -180.0, 180.0):
        LAYOUT.SKY().SetSunPos(sun_pos[0][0], sun_pos[1][0])
    if IMGUI.SliderFloat('sun_latitude2', '緯度', sun_pos[1], 0.0, 90.0):
        LAYOUT.SKY().SetSunPos(sun_pos[0][0], sun_pos[1][0])
    IMGUI.Separator()
    IMGUI.Text("フォグの種類")
    for key, name in fogdict.items():
        IMGUI.SameLine()
        if IMGUI.RadioButton('btnfog{}'.format(key), name, fogtype, key):
            LAYOUT.SKY().SetFog(key, fog_amount, 0)
    IMGUI.Separator()
    if IMGUI.SliderFloat('fogslider', '霧の量', fog_amount_list, 0.0, 1.0):
        LAYOUT.SKY().SetFog(fogtype[0], fog_amount_list[0], 0)
    IMGUI.End()