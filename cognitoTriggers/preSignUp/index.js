const axios = require('axios');

module.exports.handler = async event => {

  const config = {
    headers: {
      'x-api-key': 'YFrR9r5nSR2KkP5VMwhYwaQ6oV14bHjl1uZSytHo'
    }
  }

  try {
    console.log(event.userName)
    const response = await axios.post('https://gollbqzbfc.execute-api.ap-southeast-1.amazonaws.com/prod/verifyWallet', {
    "publicAddress": event.userName
    }, config);
    console.log(response.data, response.status)
    event.response.autoConfirmUser = true;
    return event;
  } catch(err) {
    console.log(err.response)
    if (err.response) {
      if (err.response.status === 404) {
        throw new Error('[404] Invalid Wallet Account');
      } else {
        throw new Error('[500] Internal Server Error');
      }
    }
  }
};