Page({

  data: {
    N: 0,
    L: 1,
    SNR: 2,
    init_value: 0.0,
    channel: "BEC",
    algorithm: "SC",
    data_list: {},
  },
  JumpToPage: function (e) {
    let that = this;
    console.log("N = ", this.data.N, " init_value = ", this.data.init_value)
    console.log("L = ", this.data.L, " channel = ", this.data.channel)
    console.log("algorithm = ", this.data.algorithm, "SNR = ", this.data.SNR)
    let SN = "N="+this.data.N + "&&"
    let Sinitvalue = "init_value="+this.data.init_value + "&&"
    let SL = "L="+this.data.L + "&&"
    let SSNR = "SNR="+this.data.SNR + "&&"
    let Schannel = "channel="+this.data.channel + "&&"
    let Salgorithm = "algorithm="+this.data.algorithm
    tt.request({
      url: "http://172.26.147.150:5000/?" + SN + Sinitvalue + SL + SSNR + Schannel + Salgorithm,
      success:function(res){
        let Data = res.data
        console.log("success", Data)
        that.data.data_list = Data
      },
      fail: function(e) {
        console.log("fail", e)
      }
    })
  },


  Start: function(e) {
    console.log(this.data.data_list)
    this.setData({
        A : this.data.data_list["A"],
        B : this.data.data_list["B"],
        C : this.data.data_list["C"],
        D : this.data.data_list["D"],
        E : this.data.data_list["E"]
    })

  },

  inputN: function (e) {
    this.data.N = e.detail.value
  },
  inputInit_value: function (e) {
    this.data.init_value = e.detail.value
  },
  inputL: function (e) {
    this.data.L = e.detail.value
  },
  inputSNR: function (e) {
    this.data.SNR = e.detail.value
  },
  Change_channel: function (e) {
    this.data.channel = e.detail.value
  },
  Change_algorithm: function (e) {
    this.data.algorithm = e.detail.value
  },


});