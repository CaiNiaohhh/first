Page({

  data: {
    N: 0,
    L: 1,
    SNR: 2,
    bec_err:0.3,
    init_value: 0.0,
    channel: "BEC",
    algorithm: "SC",
    data_list: {},
  },
  JumpToPage: function (e) {
    let that = this;
    console.log("N = ", this.data.N, " init_value = ", this.data.init_value, " bec_err = ", this.data.bec_err)
    console.log("L = ", this.data.L, " channel = ", this.data.channel)
    console.log("algorithm = ", this.data.algorithm, "SNR = ", this.data.SNR)
    let SN = "N="+this.data.N + "&&"
    let Sinitvalue = "init_value="+this.data.init_value + "&&"
    let SL = "L="+this.data.L + "&&"
    let SSNR = "SNR="+this.data.SNR + "&&"
    let Sbec_err = "bec_err="+this.data.bec_err + "&&"
    let Schannel = "channel="+this.data.channel + "&&"
    let Salgorithm = "algorithm="+this.data.algorithm
    tt.request({
      url: "http://127.0.0.1:5000/?" + SN + Sinitvalue + SL + SSNR + Sbec_err + Schannel + Salgorithm,
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
  input_bec_err: function (e) {
    this.data.bec_err = e.detail.value
  },
  Change_channel: function (e) {
    this.data.channel = e.detail.value
  },
  Change_algorithm: function (e) {
    this.data.algorithm = e.detail.value
  },


});