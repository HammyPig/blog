---
icon: "{fas}`cloud`"
date: "2025-08-09"
---

# Using Rclone and Backblaze B2 for Reliable Encrypted Cloud Storage

## Prelude

If you have fallen victim to the vague unreliable behaviour of mainstream cloud storage, then this solution is for you. Rclone is a no-nonsense solution done entirely through explicit command-line instruction, providing inherit encryption, robust upload verification, and transparent feedback at every step. Together with Backblaze B2, it provides the forever solution to long-term archival cloud storage.

## Setup

- [Create a Backblaze account](https://www.backblaze.com/docs/cloud-storage-enable-backblaze-b2)
- [Create a new bucket](https://www.backblaze.com/docs/cloud-storage-create-and-manage-buckets)
- [Link rclone with the Backblaze bucket](https://rclone.org/b2/)
- Encrypt your storage by [wrapping a Crypt remote around the Backblaze remote](https://rclone.org/crypt/)

Once completed, you will be given an empty root folder with the name of your bucket, located at `secret:<bucket>`. Any files and folders you then upload will be stored like normal, e.g. `secret:<bucket>/example_folder/example_file.txt`.

## Basic Workflow

- List the contents of your root folder: `rclone lsf secret:<bucket>`
- Upload your first folder: `rclone copy <example_folder> secret:<bucket>/<example_folder>`
- Verify the upload completed: `rclone cryptcheck <example_folder> secret:<bucket>/<example_folder>`
- Delete the local folder to save storage
- Later...
- Check the size of the uploaded folder: `rclone size secret:<bucket>/<example_folder>`
- Download the cloud folder when needed: `rclone copy secret:<bucket>/<example_folder> <example_folder>`

Uploads/downloads will skip files which have already been processed. This means you can stop an operation and then resume it later, or run an operation multiple times to quickly verify every file has been processed.

## Fundamental Commands

### List contents of a folder

```sh
rclone lsf secret:<bucket>/<folder>
```

Shows files and folders inside target folder.

### Upload/download a folder

```sh
rclone copy <folder> secret:<bucket>/<folder>
```

Uploads **the contents** of the source folder **into** the destination folder

- Creates the destination folder if it does not exist.
- Will skip uploading contents that are already found in the destination folder.

To then download a folder, simply switch the order:

```sh
rclone copy secret:<bucket>/<folder> <folder>
```

### Verify two folders have the same contents

```sh
rclone cryptcheck <folder> secret:<bucket>/<folder>
```

Will print out the number of missing/existing files, and the total differences. A perfect copy will have zero differences.

### Check the size of an uploaded folder

```sh
rclone size secret:<bucket>/<folder>
```

Prints the size of the target folder.
