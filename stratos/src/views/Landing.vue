<template>
  <v-app>
    <v-content id="main-background">
      <v-app-bar color="transparent" class="ma-8 elevation-0" app>
        <v-container>
          <v-row class="text-uppercase logo-text">
            <v-icon x-large>mdi-balloon</v-icon>
            <span class="font-weight-bold">STRATOS</span>
            <span class="font-weight-light">PHERE</span>
            <v-spacer></v-spacer>
            <v-btn to="/" text>Home</v-btn>
            <v-btn to="/upload" text>Upload</v-btn>
            <v-btn to="/visualizer" text>Visualize</v-btn>
          </v-row>
        </v-container>
      </v-app-bar>
      <v-container class="fill-height" fluid>
        <v-row align="start" justify="center">
          <v-col cols="12" sm="8" md="5">
            <v-card color="transparent" class="elevation-0">
              <v-row align="center" justify="center">
                <v-col cols="6">
                  <v-hover>
                    <v-card @mouseover="hover = true" @mouseleave="hover = false" class="elevation-8">
                      <v-img src="@/assets/balloon.jpeg"></v-img>
                      <v-fade-transition>
                        <v-overlay v-if="hover" absolute>
                          <v-btn href="http://www.asc-csa.gc.ca/eng/sciences/balloons/default.asp">Tell me more about the balloons</v-btn>
                        </v-overlay>
                      </v-fade-transition>
                    </v-card>
                  </v-hover>
                </v-col>
                <v-col cols="6">
                  <v-card flat color="transparent" class="pa-7">
                    <h1>Visualize the Data</h1>
                    <p>See what the balloon saw on its journey to the <i>Stratosphere</i></p>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn outlined to="/visualizer">Go to the visualizer</v-btn>
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
    <v-footer app color="transparent" justify="center">
      <v-container>
        <v-row>
          <v-img height="50px" aspect-ratio="1" src="@/assets/csa.png" contain></v-img>
          <v-spacer></v-spacer>
          <p style="color: black">&copy; The EH Team 2019</p>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
    export default {
        name: 'landing',
        data: () => ({
            hover: false
        })
    }
</script>

<style lang="scss">
  #main-background {
    background: linear-gradient(to bottom, #033a5e 0%, #a1b8c3 100%);
  }

  .logo-text {
    font-size: 38px;
  }
</style>
