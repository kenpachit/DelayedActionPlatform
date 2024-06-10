import Web3 from 'web3';
import axios from 'axios';
import { abi } from './DelayedActionPlatformContractABI'; 

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;
const API_BASE_URL = process.env.API_BASE_URL;
const ETHEREUM_NODE_URL = process.env.ETHEREUM_NODE_URL;

const web3 = new Web3(new Web3.providers.HttpProvider(ETHEREUM_NODE_URL));

const delayedActionContract = new web3.eth.Contract(abi, CONTRACT_ADDRESS);

const submitAction = async (fromAddress, privateKey, actionDetails, scheduleTime) => {
    const transaction = delayedActionContract.methods.scheduleAction(actionDetails, scheduleDate.getTime());
    const signedTx = await web3.eth.accounts.signTransaction({
        to: CONTRACT_ADDRESS,
        data: transaction.encodeABI(),
        gas: '1000000',
    }, privateKey);
    const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
    console.log(`Transaction hash: ${receipt.transactionHash}`);
};

const fetchScheduledActions = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/scheduledActions`);
        if (response.data && response.data.length > 0) {
            console.log(response.data);
        } else {
            console.log('No scheduled actions found.');
        }
    } catch (error) {
        console.error('An error occurred while fetching scheduled actions:', error);
    }
};

const scheduleActionFormSubmit = async (event) => {
    event.preventDefault();
    const form = document.getElementById('actionForm');
    const fromAddress = form.elements['fromAddress'].value;
    const privateKey = form.elements['privateKey'].value;
    const actionDetails = form.elements['actionDetails'].

    const scheduleTime = new Date(form.elements['scheduleOSiteptionTime'].value);

    await submitAction(fromAddress, privateKey, actionDetails, scheduleTime);
};

document.getElementById('actionForm').addEventListener('submit', scheduleActionFormSubmit);

fetchScheduledActions();