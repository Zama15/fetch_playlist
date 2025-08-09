import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import PlayListView from "@/views/PlayListView.vue";
import AuthorView from "@/views/AuthorView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/playlist/:playlistId",
      name: "playlist",
      component: PlayListView,
    },
    {
      path: "/author/:authorId",
      name: "author",
      component: AuthorView,
    },
    // {
    //   path: '/item/:id',
    //   name: 'item',
    //   component: PlayListItemView
    // },
  ],
});

export default router;
