# Mount an attached volume `vdb`

To access the attached volume `vdb`, you'll need to mount it. 

## Guide

Here's a step-by-step process to access the volume:

1. First, check if the volume has a file system:

   ```bash
   sudo file -s /dev/vdb
   ```

   If it shows "data", the volume doesn't have a file system yet.

2. If there's no file system, create one (e.g., ext4):

   ```bash
   sudo mkfs -t ext4 /dev/vdb
   ```

   Skip this step if a file system already exists.

3. Create a mount point:

   ```bash
   sudo mkdir /mnt/data
   ```

4. Mount the volume:

   ```bash
   sudo mount /dev/vdb /mnt/data
   ```

5. Verify the mount:

   ```bash
   df -h
   ```

   You should see `/dev/vdb` mounted on `/mnt/data`.

6. To make the mount persistent across reboots, add an entry to `/etc/fstab`:

   ```bash
   echo '/dev/vdb /mnt/data ext4 defaults 0 2' | sudo tee -a /etc/fstab
   ```

   This assumes you used ext4 as the file system. Adjust if you used a different one.

Now you can access the volume at `/mnt/data`. 
You can read and write files to this location.

To ensure you have the correct permissions:

```bash
sudo chown -R $(whoami):$(whoami) /mnt/data
```

Replace `$(whoami)` with your username if you're not currently logged in as the user who needs access.
