<template>
  <div class="flex-col">
    <LayoutHeader v-if="contact.doc">
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader>
    <div v-if="contact.doc" class="flex h-full flex-col overflow-hidden">
      <div class="flex items-center justify-start gap-6 p-5">
        <div class="group relative h-24 w-24">
          <Avatar
            size="3xl"
            class="h-24 w-24"
            :label="contact.doc.full_name"
            :image="contact.doc.image"
          />
          <FileUploader
            :validate-file="validateFile"
            @success="changeContactImage"
          >
            <template #default="{ openFileSelector, error }">
              <component
                :is="contact.doc.image ? Dropdown : 'div'"
                v-bind="
                  contact.doc.image
                    ? {
                        options: [
                          {
                            icon: 'upload',
                            label: contact.doc.image
                              ? 'Change image'
                              : 'Upload image',
                            onClick: openFileSelector,
                          },
                          {
                            icon: 'trash-2',
                            label: 'Remove image',
                            onClick: () => changeContactImage(''),
                          },
                        ],
                      }
                    : { onClick: openFileSelector }
                "
                class="!absolute inset-x-0 bottom-0"
              >
                <div
                  class="z-1 absolute inset-x-0 bottom-0 flex h-14 cursor-pointer items-center justify-center rounded-b-full bg-black bg-opacity-40 pt-3 opacity-0 duration-300 ease-in-out group-hover:opacity-100"
                  style="
                    -webkit-clip-path: inset(12px 0 0 0);
                    clip-path: inset(12px 0 0 0);
                  "
                >
                  <CameraIcon class="h-6 w-6 cursor-pointer text-white" />
                </div>
              </component>
            </template>
          </FileUploader>
        </div>
        <div class="flex flex-col gap-0.5 truncate">
          <div class="truncate text-3xl font-semibold">
            <span v-if="contact.doc.salutation">
              {{ contact.doc.salutation + ". " }}
            </span>
            <span>{{ contact.doc.full_name }}</span>
          </div>
          <div class="flex items-center gap-2 text-base text-gray-700">
            <div v-if="contact.doc.email_id" class="flex items-center gap-1.5">
              <EmailIcon class="h-4 w-4" />
              <span class="">{{ contact.doc.email_id }}</span>
            </div>
            <span
              v-if="contact.doc.email_id"
              class="text-3xl leading-[0] text-gray-600"
            >
              &middot;
            </span>
            <component
              :is="callEnabled ? Tooltip : 'div'"
              v-if="contact.doc.actual_mobile_no"
              :text="'Make Call'"
            >
              <div
                class="flex items-center gap-1.5"
                :class="callEnabled ? 'cursor-pointer' : ''"
                @click="callEnabled && makeCall(contact.doc.actual_mobile_no)"
              >
                <PhoneIcon class="h-4 w-4" />
                <span class="">{{ contact.doc.actual_mobile_no }}</span>
              </div>
            </component>
            <span
              v-if="contact.doc.actual_mobile_no"
              class="text-3xl leading-[0] text-gray-600"
            >
              &middot;
            </span>
            <div
              v-if="contact.doc.company_name"
              class="flex items-center gap-1.5"
            >
              <Avatar
                size="xs"
                :label="contact.doc.company_name"
                :image="
                  getOrganization(contact.doc.company_name)?.organization_logo
                "
              />
              <span class="">{{ contact.doc.company_name }}</span>
            </div>
            <span
              v-if="contact.doc.company_name"
              class="text-3xl leading-[0] text-gray-600"
            >
              &middot;
            </span>
            <Button
              v-if="
                contact.doc.email_id ||
                contact.doc.mobile_no ||
                contact.doc.company_name
              "
              variant="ghost"
              :label="'More'"
              class="-ml-1 cursor-pointer hover:text-gray-900"
              @click="
                () => {
                  detailMode = true;
                  showContactModal = true;
                }
              "
            />
          </div>
          <div class="mt-2 flex gap-1.5">
            <Button
              :label="'Edit'"
              size="sm"
              @click="
                () => {
                  detailMode = false;
                  showContactModal = true;
                }
              "
            >
              <template #prefix>
                <EditIcon class="h-4 w-4" />
              </template>
            </Button>
            <Button
              :label="'Delete'"
              theme="red"
              size="sm"
              @click="deleteContact"
            >
              <template #prefix>
                <FeatherIcon name="trash-2" class="h-4 w-4" />
              </template>
            </Button>
          </div>
          <ErrorMessage :message="error" />
        </div>
      </div>
    </div>
  </div>
  <ContactModal
    v-model="showContactModal"
    :contact="contact"
    :options="{ detailMode }"
  />
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import {
  Breadcrumbs,
  createDocumentResource,
  Avatar,
  Dropdown,
  FileUploader,
  call,
} from "frappe-ui";
import { LayoutHeader } from "@/components";
import { CameraIcon, EditIcon } from "@/components/icons";
import { useRouter } from "vue-router";
import { globalStore } from "@/stores/global";

const { $dialog } = globalStore();

const props = defineProps({
  contactId: {
    type: String,
    required: true,
  },
});

const router = useRouter();
const showContactModal = ref(false);
const detailMode = ref(false);

const contact = createDocumentResource({
  doctype: "Contact",
  name: props.contactId,
});

const breadcrumbs = computed(() => {
  let items = [{ label: "Contacts", route: { name: "ContactList" } }];
  items.push({
    label: contact.doc?.full_name,
    route: { name: "Contact" },
  });
  return items;
});

async function deleteContact() {
  $dialog({
    title: "Delete contact",
    message: "Are you sure you want to delete this contact?",
    actions: [
      {
        label: "Delete",
        theme: "red",
        variant: "solid",
        async onClick(close) {
          contact.delete.submit();
          close();
          router.push({ name: "Contacts" });
        },
      },
    ],
  });
}
</script>
