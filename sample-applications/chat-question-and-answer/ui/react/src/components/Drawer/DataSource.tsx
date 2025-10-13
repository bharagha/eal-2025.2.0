// Copyright (C) 2024 Intel Corporation
// SPDX-License-Identifier: Apache-2.0

import { Button, Container, Drawer, FileInput, Text, TextInput, SegmentedControl } from '@mantine/core'
import { SyntheticEvent, useState } from 'react'
import { useAppDispatch } from '../../redux/store'
import { submitDataSourceURL, uploadFile } from '../../redux/Conversation/ConversationSlice'

type Props = {
  opened: boolean
  onClose: () => void
}

export default function DataSource({ opened, onClose }: Props) {
  const title = "Data Source"
  const [file, setFile] = useState<File | null>();
  const [uploadMethod, setUploadMethod] = useState<string>('file');
  const [url, setURL] = useState<string>("");
  const dispatch = useAppDispatch()

  const handleFileUpload = () => {
    if (file) {
      dispatch(uploadFile({ file }));
    }
  };

  const handleURLSubmit = () => {
    if (url) {
      dispatch(submitDataSourceURL({ link_list: url.split(";") }));
    }
  };

  const handleChange = (event: SyntheticEvent) => {
    event.preventDefault()
    setURL((event.target as HTMLTextAreaElement).value)
  }

  return (
    <Drawer title={title} position="right" opened={opened} onClose={onClose} withOverlay={false}>
      <Text size="sm">
        Please upload your local file or paste a remote file link, and Chat will respond based on the content of the uploaded file.
      </Text>

      <Container styles={{
        root: { paddingTop: '40px', display:'flex', flexDirection:'column', alignItems:'center' }
      }}>
        <SegmentedControl
          value={uploadMethod}
          onChange={setUploadMethod}
          data={[
            { label: 'Upload File', value: 'file' },
            { label: 'Use Link', value: 'url' }
          ]}
          size="sm"
        />
      </Container>

      <Container styles={{root:{paddingTop: '40px'}}}>
        <div>
          {uploadMethod === 'file' ? (
            <>
              <FileInput 
                value={file} 
                onChange={setFile}
                placeholder="Choose File" 
                description={"Choose a file to upload for RAG"}
              />
              <Button 
                style={{marginTop:'10px'}} 
                onClick={handleFileUpload} 
                disabled={!file}
                size="sm"
              >
                Upload File
              </Button>
            </>
          ) : (
            <>
              <TextInput 
                value={url} 
                onChange={handleChange} 
                placeholder='URL' 
                description={"Use semicolons (;) to separate multiple URLs"} 
              />
              <Button 
                style={{marginTop:'10px'}} 
                onClick={handleURLSubmit} 
                disabled={!url}
                size="sm"
              >
                Submit URLs
              </Button>
            </>
          )}
        </div>
      </Container>
    </Drawer>
  )
}
