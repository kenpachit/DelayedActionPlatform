import Web3 from 'web3';
import axios from 'axios';
import { abi } from './DelayedActionPlatformContractABI';

const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;
const API_BASE_URL = process.env.API_BASE_URL;
const ETHEREUM_NODE_URL = process.env.ETHEREUM_NODE_URL;

const web3 = new Web3(new Web3.providers.HttpProvider(ETHEREUM_NODE_URL));

const delayedActionContract = new web3.eth.Contract(abi, CONTRACT_ADDRESS);

let cachedScheduledActions = null;
let lastFetchTime = null;
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

const submitAction = async (fromAddress, privateKey, actionDetails, scheduleTime) => {
    try {
        const transaction = delayedActionContract.methods.scheduleAction(actionDetails, scheduleTime.getTime());
        const signedTx = await web3.eth.accounts.signTransaction({
            to: CONTRACT_ADDRESS,
            data: transaction.encodeABI(),
            gas: '1000000',
        }, privateKey);
        const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
        console.log(`Transaction hash: ${receipt.transactionHash}`);
    } catch (error) {
        console.error('An error occurred while submitting the action:', error);
    }
    cachedScheduledActions = null;
};

const fetchScheduledActions = async () => {
    const currentTime = new Date().getTime();
    if (cachedScheduledActions !== null && lastFetchTime !== null && (currentTime - lastFetchTime) < CACHE_DURATION) {
        console.log(cachedScheduledActions);
        return;
    }
    try {
        const response = await axios.get(`${API_BASE_URL}/scheduledActions`);
        if (response.data && response.data.length > 0) {
            cachedScheduledActions = response.data;
            lastFetchTime = currentTime;
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
    try {
        const form = document.getElementById('actionForm');
        const fromAddress = form.elements['fromAddress'].value;
        const privateKey = form.elements['privateKey'].value;
        const actionDetails = form.elements['actionDetails'].value;
        const scheduleTime = new Date(form.elements['scheduleTime'].value); // Ensure the element's name matches exactly

        await submitAction(fromAddress, privateKey, actionDetails, scheduleCoordinatesTime);
    } catch (error) {
        console.error('Error handling form submission:', error);
    }
};

document.getElementById('actionForm').addEventListener('submit', scheduleActionFormSubmit);

fetchScheduledActions();