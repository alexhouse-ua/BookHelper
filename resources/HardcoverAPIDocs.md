This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where security check has been disabled.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Security check has been disabled - content may contain sensitive information
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.github/
  ISSUE_TEMPLATE/
    bug_report.md
    feature_request.md
  workflows/
    deploy.yml
  pull_request_template.md
public/
  favicon.svg
src/
  assets/
    hardcover.svg
  components/
    GraphQLExplorer/
      GraphQLExplorer.astro
      GraphQLRunner.tsx
      JSONResults.test.jsx
      JSONResults.tsx
      StatusMessages.test.jsx
      StatusMessages.tsx
      TableResults.test.jsx
      TableResults.tsx
    ui/
      accordion.tsx
      button.tsx
      card.tsx
      input.tsx
      label.tsx
      popover.tsx
      scroll-area.tsx
      select.tsx
      separator.tsx
      table.tsx
      tabs.tsx
      textarea.tsx
    APIBanner.tsx
    EditLink.tsx
    index.tsx
    LibrarianBanners.tsx
    PageEdit.astro
    SocialIcons.astro
  content/
    docs/
      api/
        GraphQL/
          Schemas/
            Activities.mdx
            Authors.mdx
            Books.mdx
            Characters.mdx
            Contributions.mdx
            Countries.mdx
            Editions.mdx
            Goals.mdx
            Images.mdx
            Languages.mdx
            Likes.mdx
            Lists.mdx
            Notifications.mdx
            Platforms.mdx
            Prompts.mdx
            Publishers.mdx
            ReadingFormats.mdx
            ReadingJournals.mdx
            Recommendations.mdx
            Series.mdx
            Tags.mdx
            Users.mdx
        guides/
          GettingAllBooksInLibrary.mdx
          GettingBookDetails.mdx
          GettingBooksProgress.mdx
          GettingBooksWithStatus.mdx
          Searching.mdx
          UpdatingABooksProgress.mdx
          UpdatingReadingJournal.mdx
        Getting-Started.mdx
      contributing/
        API-Docs.mdx
        Astro-Components.mdx
        Frontmatter.mdx
        index.mdx
        Librarian-Guides.mdx
        React-Components.mdx
        Translating-Documentation.mdx
        Using-Translations.mdx
      it/
        api/
          GraphQL/
            Schemas/
              Activities.mdx
              Authors.mdx
              Books.mdx
              Characters.mdx
              Contributions.mdx
              Countries.mdx
              Editions.mdx
              Goals.mdx
              Images.mdx
              Languages.mdx
              Likes.mdx
              Lists.mdx
              Notifications.mdx
              Platforms.mdx
              Prompts.mdx
              Publishers.mdx
              ReadingFormats.mdx
              ReadingJournals.mdx
              Recommendations.mdx
              Series.mdx
              Tags.mdx
              Users.mdx
          guides/
            GettingAllBooksInLibrary.mdx
            GettingBookDetails.mdx
            GettingBooksProgress.mdx
            GettingBooksWithStatus.mdx
            Searching.mdx
            UpdatingABooksProgress.mdx
            UpdatingReadingJournal.mdx
          Getting-Started.mdx
        contributing/
          API-Docs.mdx
          Astro-Components.mdx
          Doc-Translations.mdx
          Frontmatter.mdx
          Librarian-Guides.mdx
          React-Components.mdx
          Using-Translations.mdx
        librarians/
          Resources/
            ISBNAndASIN.mdx
          Standards/
            AuthorStandards.mdx
            BookStandards.mdx
            ComicStandards.mdx
            EditionStandards.mdx
            SeriesStandards.mdx
          Editing.mdx
          FAQ.mdx
          Getting-Started.mdx
        404.mdx
        index.mdx
        ui.json
      librarians/
        Resources/
          ISBNAndASIN.mdx
        Standards/
          AuthorStandards.mdx
          BookStandards.mdx
          ComicStandards.mdx
          Editing-FAQ.mdx
          EditionStandards.mdx
          MergingStandards.mdx
          SeriesStandards.mdx
        FAQ.mdx
        Getting-Started.mdx
      404.mdx
      index.mdx
      ui.json
    config.ts
  layouts/
    documentation.astro
    librarians.astro
  lib/
    translations.ts
    utils.test.ts
    utils.ts
  Consts.ts
  env.d.ts
  tailwind.css
  types.ts
.gitignore
.nvmrc
astro.config.mjs
components.json
CONTRIBUTING.md
DEVELOPERS.md
LICENSE.md
package.json
README.md
tailwind.config.mjs
tsconfig.json
vitest-setup.js
vitest.config.ts
```

# Files

## File: .github/ISSUE_TEMPLATE/bug_report.md
````markdown
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Desktop (please complete the following information):**
 - OS: [e.g. iOS]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]

**Smartphone (please complete the following information):**
 - Device: [e.g. iPhone6]
 - OS: [e.g. iOS8.1]
 - Browser [e.g. stock browser, safari]
 - Version [e.g. 22]

**Additional context**
Add any other context about the problem here.
````

## File: .github/ISSUE_TEMPLATE/feature_request.md
````markdown
---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: ''
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
````

## File: .github/workflows/deploy.yml
````yaml
name: Deploy to GitHub Pages

on:
  # Trigger the workflow every time you push to the `main` branch
  # Using a different branch name? Replace `main` with your branch’s name
  push:
    branches: [main]
  # Allows you to run this workflow manually from the Actions tab on GitHub.
  workflow_dispatch:

# Allow this job to clone the repo and create a page deployment
permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout your repository using git
        uses: actions/checkout@v4
      - name: Install, build, and upload your site output
        uses: withastro/action@v2
          # with:
          # path: . # The root location of your Astro project inside the repository. (optional)
          # node-version: 20 # The specific version of Node that should be used to build your site. Defaults to 18. (optional)
          # package-manager: pnpm@latest # The Node package manager that should be used to install dependencies and build your site. Automatically detected based on your lockfile. (optional)
      - name: 'Test'
        run: npx vitest --coverage.enabled true
      - name: "Upload Coverage"
        uses: actions/upload-artifact@v4
        with:
          name: coverage-main
          path: coverage
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
````

## File: .github/pull_request_template.md
````markdown
# Description
Include a summary of the change, relevant motivation, context, and images/videos.

- If this is a new content, describe the content and where it should be placed.
- If this is an updated content, describe the changes and where they should be placed.
- If this is a deleted content, describe the content and why it should be removed.

- If this is a broken link, provide what the link should be and where it should go.

- If this is a new feature, describe the feature and how it should work.
- Is there a link to the issue or feature request that this PR solves?

- If this is other, describe the change and why it should be made.


# Hardcover or Discord Username
Include your Hardcover or discord usernames so we can find you and follow up if needed.

# Types of changes
- [ ] New content
- [ ] Updated content
- [ ] Deleted content
- [ ] Broken link
- [ ] Bug fix
- [ ] New feature
- [ ] Other

# Checklist:
- [ ] I have read the [CONTRIBUTING](https://github.com/hardcoverapp/hardcover-docs/blob/main/CONTRIBUTING.md) document.
- [ ] I have explained why the change is necessary and how it fits into the existing content.
- [ ] I have communicated this change in the [#API](https://discord.com/channels/835558721115389962/1278040045324075050) or [#librarians](https://discord.com/channels/835558721115389962/1105918193022812282) discord channels.

# How to test it?
If this is a new feature or bug fix, describe how to test it.
- Describe how to navigate to the changed content and what to look for.
- Describe how to test the new feature or bug fix, and what the expected outcome is.
- List any additional steps that should be taken to verify the change.
- Have you added any new automatic tests to verify the change?
````

## File: public/favicon.svg
````
<svg xmlns="http://www.w3.org/2000/svg" class="w-9 group-hover:rotate-12 transition-all duration-300" fill="none" viewBox="0 0 40 40"><path d="M12.8889 32.5982C12.666 31.7661 13.1598 30.9108 13.9919 30.6879L30.2971 26.3189C31.1292 26.096 31.9845 26.5898 32.2075 27.4219L32.8739 29.9089C33.1711 31.0183 32.5127 32.1587 31.4033 32.456L18.1113 36.0176C15.8924 36.6121 13.6116 35.2953 13.0171 33.0764L12.8889 32.5982Z" fill="#4F46E5"></path><path d="M7.62314 12.946C7.05137 10.8121 8.3177 8.61876 10.4516 8.04699L16.8851 32.0571L13.0214 33.0924L7.62314 12.946Z" fill="#4F46E5"></path><path d="M29.3358 24.432L31.2677 23.9144L32.3584 27.985C32.6443 29.052 32.0111 30.1486 30.9442 30.4345L29.3358 24.432Z" fill="#4338CA"></path><path d="M26.4446 5.91475C26.1474 4.80529 25.007 4.14688 23.8975 4.44416L10.5286 8.02636C9.41911 8.32364 8.7607 9.46403 9.05798 10.5735L14.9532 32.5748L22.6461 30.5135C23.1986 30.3654 23.5265 29.7975 23.3785 29.245C23.2304 28.6925 23.5583 28.1245 24.1108 27.9765L29.7949 26.4535C30.9043 26.1562 31.5628 25.0158 31.2655 23.9063L26.4446 5.91475Z" fill="#6366F1"></path><path d="M21.0947 11.2811C21.145 10.6645 21.9408 10.4512 22.2927 10.9601L22.442 11.1761C22.5512 11.3341 22.724 11.4365 22.9151 11.4565L23.2375 11.4902C23.838 11.553 24.0445 12.3235 23.5558 12.6781L23.2935 12.8685C23.138 12.9813 23.0395 13.1564 23.0239 13.3479L23.0026 13.6096C22.9523 14.2262 22.1564 14.4394 21.8046 13.9306L21.6553 13.7146C21.546 13.5566 21.3732 13.4542 21.1821 13.4342L20.8598 13.4005C20.2592 13.3377 20.0528 12.5672 20.5415 12.2126L20.8038 12.0222C20.9593 11.9094 21.0577 11.7343 21.0734 11.5428L21.0947 11.2811Z" fill="#312E81"></path><path d="M18.3031 16.3181C18.3533 15.7015 19.1492 15.4882 19.501 15.9971L20.5634 17.5337C20.6727 17.6917 20.8455 17.7941 21.0366 17.8141L22.9139 18.0104C23.5144 18.0732 23.7208 18.8436 23.2321 19.1983L21.7045 20.3069C21.549 20.4197 21.4506 20.5949 21.435 20.7863L21.2832 22.6482C21.2329 23.2649 20.4371 23.4781 20.0852 22.9692L19.0228 21.4327C18.9136 21.2747 18.7407 21.1722 18.5497 21.1522L16.6724 20.956C16.0719 20.8932 15.8654 20.1227 16.3541 19.7681L17.8817 18.6594C18.0372 18.5466 18.1357 18.3715 18.1513 18.18L18.3031 16.3181Z" fill="#312E81"></path><path d="M14.9532 32.5748C14.6571 31.4697 15.3129 30.3339 16.4179 30.0378L29.8719 26.4328L30.9441 30.4345L17.4902 34.0395C16.3851 34.3356 15.2493 33.6798 14.9532 32.5748Z" fill="#EEF2FF"></path></svg>
````

## File: src/assets/hardcover.svg
````
<svg xmlns="http://www.w3.org/2000/svg" class="w-9 group-hover:rotate-12 transition-all duration-300" fill="none" viewBox="0 0 40 40"><path d="M12.8889 32.5982C12.666 31.7661 13.1598 30.9108 13.9919 30.6879L30.2971 26.3189C31.1292 26.096 31.9845 26.5898 32.2075 27.4219L32.8739 29.9089C33.1711 31.0183 32.5127 32.1587 31.4033 32.456L18.1113 36.0176C15.8924 36.6121 13.6116 35.2953 13.0171 33.0764L12.8889 32.5982Z" fill="#4F46E5"></path><path d="M7.62314 12.946C7.05137 10.8121 8.3177 8.61876 10.4516 8.04699L16.8851 32.0571L13.0214 33.0924L7.62314 12.946Z" fill="#4F46E5"></path><path d="M29.3358 24.432L31.2677 23.9144L32.3584 27.985C32.6443 29.052 32.0111 30.1486 30.9442 30.4345L29.3358 24.432Z" fill="#4338CA"></path><path d="M26.4446 5.91475C26.1474 4.80529 25.007 4.14688 23.8975 4.44416L10.5286 8.02636C9.41911 8.32364 8.7607 9.46403 9.05798 10.5735L14.9532 32.5748L22.6461 30.5135C23.1986 30.3654 23.5265 29.7975 23.3785 29.245C23.2304 28.6925 23.5583 28.1245 24.1108 27.9765L29.7949 26.4535C30.9043 26.1562 31.5628 25.0158 31.2655 23.9063L26.4446 5.91475Z" fill="#6366F1"></path><path d="M21.0947 11.2811C21.145 10.6645 21.9408 10.4512 22.2927 10.9601L22.442 11.1761C22.5512 11.3341 22.724 11.4365 22.9151 11.4565L23.2375 11.4902C23.838 11.553 24.0445 12.3235 23.5558 12.6781L23.2935 12.8685C23.138 12.9813 23.0395 13.1564 23.0239 13.3479L23.0026 13.6096C22.9523 14.2262 22.1564 14.4394 21.8046 13.9306L21.6553 13.7146C21.546 13.5566 21.3732 13.4542 21.1821 13.4342L20.8598 13.4005C20.2592 13.3377 20.0528 12.5672 20.5415 12.2126L20.8038 12.0222C20.9593 11.9094 21.0577 11.7343 21.0734 11.5428L21.0947 11.2811Z" fill="#312E81"></path><path d="M18.3031 16.3181C18.3533 15.7015 19.1492 15.4882 19.501 15.9971L20.5634 17.5337C20.6727 17.6917 20.8455 17.7941 21.0366 17.8141L22.9139 18.0104C23.5144 18.0732 23.7208 18.8436 23.2321 19.1983L21.7045 20.3069C21.549 20.4197 21.4506 20.5949 21.435 20.7863L21.2832 22.6482C21.2329 23.2649 20.4371 23.4781 20.0852 22.9692L19.0228 21.4327C18.9136 21.2747 18.7407 21.1722 18.5497 21.1522L16.6724 20.956C16.0719 20.8932 15.8654 20.1227 16.3541 19.7681L17.8817 18.6594C18.0372 18.5466 18.1357 18.3715 18.1513 18.18L18.3031 16.3181Z" fill="#312E81"></path><path d="M14.9532 32.5748C14.6571 31.4697 15.3129 30.3339 16.4179 30.0378L29.8719 26.4328L30.9441 30.4345L17.4902 34.0395C16.3851 34.3356 15.2493 33.6798 14.9532 32.5748Z" fill="#EEF2FF"></path></svg>
````

## File: src/components/GraphQLExplorer/GraphQLExplorer.astro
````
---
import {Code, Tabs, TabItem} from '@astrojs/starlight/components';
import {useTranslation, getPreference, setPreference} from "../../lib/utils";
import {GraphQLRunner} from './GraphQLRunner.tsx';

const locale = Astro.currentLocale;

const {
    query,
    description = '',
    canTry = true,
    presentation = undefined, // Undefined will default to the user's preference
    forcePresentation = false,
    title = useTranslation("ui.graphQLExplorer.example", locale)
} = Astro.props;

// Is the query a mutation?
// If so, we don't allow it to run it in the explorer,
// and we don't show the "Try it Yourself" tab
const isMutation = query.trim().includes('mutation');
---

<Tabs>
    <TabItem label={useTranslation("ui.graphQLExplorer.query", locale)} icon="document">
        {query && (
                <Code lang="graphql" title={title} code={query} wrap={true}/>
        )}
        {!query && (
                <Code lang="graphql" title={title}
                      code={useTranslation("ui.graphQLExplorer.statusMessages.emptyQuery", locale)}/>
        )}
    </TabItem>
    {canTry && !isMutation && (
            <TabItem label={useTranslation("ui.graphQLExplorer.tryIt", locale)} icon="seti:graphql">
                <div class="not-content">
                    <GraphQLRunner query={query}
                                   description={description}
                                   presentation={presentation}
                                   forcePresentation={forcePresentation ? presentation : null}
                                   locale={locale}
                                   client:only="react" />
                </div>
            </TabItem>
    )}
</Tabs>
````

## File: src/components/GraphQLExplorer/GraphQLRunner.tsx
````typescript
import {Button} from "@/components/ui/button.tsx";
import {Label} from "@/components/ui/label.tsx";
import {ScrollArea} from "@/components/ui/scroll-area.tsx";
import {Textarea} from "@/components/ui/textarea.tsx";
import {URLS} from "@/Consts";
import {useTranslation, getPreference, setPreference} from "@/lib/utils.ts";
import React, {useEffect, useState} from "react";
import {LuCode, LuKeyRound, LuLoader, LuTable, LuTerminal} from "react-icons/lu";
import {JSONResults} from "./JSONResults.tsx";
import {StatusMessages} from "./StatusMessages.tsx";
import {TableResults} from "./TableResults.tsx";

export const GraphQLRunner = (props: {
    query: string, description?: string,
    presentation?: 'json' | 'table' | undefined, // If not provided, will use the default from user preferences
    forcePresentation?: 'json' | 'table' | undefined
    locale?: string
}) => {
    const {description, forcePresentation, locale = 'en'} = props;
    let {presentation} = props;

    if (!presentation) {
        presentation = getPreference('graphQLResults');
    }

    // Get the query from props so we can modify it
    const [query, setQuery] = useState(props.query);

    // Get the auth token and user_id from local storage if it exists
    const localAuthToken = window.localStorage.getItem('auth_token');
    const [userId, setUserId] = useState(window.localStorage.getItem('user_id') || '');
    const [authToken, setAuthToken] = useState(localAuthToken || '');

    // If the query is a mutation, we don't allow it to be run here, and instead we will show a message to the user
    const isMutation = query.trim().toLowerCase().includes('mutation');

    // If the query has been run, we need to store the results in the React state
    const [queryStatus, setQueryStatus] = useState<'running' | 'success' | 'error' | 'idle'>('idle');
    const [queryError, setQueryError] = useState<string | undefined>();
    const [queryResults, setQueryResults] = useState<any>(null);

    const [showAuthToken, setShowAuthToken] = useState(!authToken);
    const [showQuery, setShowQuery] = useState(true);
    const [explicitQuery, setExplicitQuery] = useState(false);

    const [currentPresentation, setCurrentPresentation] = useState(forcePresentation ? forcePresentation : presentation || 'json');

    /**
     * This function will replace the ##USER_ID## token in the query with the actual user_id.
     * Additional tokens can be added here as needed.
     * @param query - string
     * @returns {string}
     */
    const ReplaceQueryTokens = (query: string): string => {
        if (!!userId) {
            // Replace the user_id token with the actual user_id
            query = query.replace(/##USER_ID##/g, userId);
        }

        return query;
    }

    useEffect(() => {
        // Replace the tokens in the query
        // Use the original query from props to ensure can this can be re-run if data changes
        setQuery(ReplaceQueryTokens(props.query));
    }, [userId]);

    /**
     * This function will handle the query using fetch.
     * In an actual application, you would want to use something like apollo-client to handle this.
     * @param runningQuery - string | undefined
     * @param keepQuery - boolean
     * @returns {Promise<any>}
     */
    const handleQueryWithFetch = (runningQuery: string | undefined, keepQuery = false): {
        then(resolve: any, reject: any): void;
    } => {
        return {
            then(resolve: any, reject: any) {
                // Ensure the auth token is provided
                if (!authToken || !authToken.trim()) {
                    reject(new Error(useTranslation("ui.graphQLExplorer.statusMessages.emptyToken", locale)));
                    return;
                }

                // If the query is a mutation, we don't allow it to be run here, and instead we will show a message to the user
                if (isMutation) {
                    reject(new Error(useTranslation("ui.graphQLExplorer.statusMessages.mutationQueryNotAllowed", locale)));
                    return;
                }

                // Ensure the query is not empty
                if (!runningQuery || !runningQuery.trim()) {
                    reject(new Error(useTranslation("ui.graphQLExplorer.statusMessages.emptyQuery", locale)));
                    return;
                }

                // Call the GraphQL endpoint with the query using fetch
                fetch(URLS.GRAPHQL_URL, {
                    method: 'POST', headers: {
                        'Content-Type': 'application/json',
                        'Authorization': authToken.startsWith('Bearer') ? authToken : `Bearer ${authToken}`
                    }, body: JSON.stringify({
                        query: runningQuery
                    })
                }).then(res => {
                    // If the response is not ok, reject the promise
                    if (!res.ok) {
                        reject(new Error(useTranslation("ui.graphQLExplorer.statusMessages.errorRunning", locale)));
                        return;
                    }

                    // Parse the JSON response
                    res.json().then(data => {
                        // If there is an error in the response, reject the promise
                        if (data.error) {
                            console.error({error: data.error});
                            reject(new Error(data.error));
                        }

                        if (data.errors) {
                            console.error({errors: data.errors});

                            // If there is a message in the errors, reject the promise with the message
                            if (data.errors[0].message) {
                                reject(new Error(data.errors[0].message));
                                return;
                            }

                            // If there is no message, reject the promise a generic error message
                            reject(new Error(useTranslation("ui.graphQLExplorer.statusMessages.errorRunning", locale)));
                        }

                        if (!explicitQuery && !keepQuery) {
                            // If the query was not explicitly set, hide the query
                            setShowQuery(false);
                        }

                        // Return the data from the query
                        resolve(data);
                    });
                }, () => {
                    // If there is an error with the fetch request, reject the promise
                    reject(new Error(useTranslation("ui.graphQLExplorer.statusMessages.connectionError", locale)));
                });
            }
        };
    };

    /**
     * This function will handle the onChange event for the auth token input field.
     * We need to update the auth token in the React state to be able to display it.
     * @param event - React.ChangeEvent<HTMLTextAreaElement>
     * @returns {void}
     */
    const updateAuthTokenUI = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
        // Get the new auth token from the input field and trim it
        const newAuthToken = event.target?.value?.trim();

        // Update the React state with the new auth token to be able to display it
        setAuthToken(newAuthToken);
    }

    /**
     * This function will handle the onBlur event for the auth token input field.
     * We are using blur instead of change to ensure the user has finished typing before we test the auth token.
     * @param event - React.ChangeEvent<HTMLTextAreaElement>
     * @returns {void}
     */
    const handleAuthTokenChange = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
        // Get the new auth token from the input field and trim it
        // This should be handled by the updateAuthTokenUI function,
        // but we are doing it here as well to be safe
        const newAuthToken = event.target?.value?.trim();

        // Query to get the user's ID
        const userIdQuery = `
            query {
                me {
                    id
                }
            }
        `;

        // Test the auth token to ensure it is valid and get the user's ID while we are at it
        handleQueryWithFetch(userIdQuery, true).then((res: any) => {
            // If the return data does not have the "me" object, the auth token is invalid
            if (!res?.data?.me) {
                console.error(useTranslation("ui.graphQLExplorer.statusMessages.invalidToken", locale));
                return;
            }

            // Only update the local storage if the auth token is valid
            window.localStorage.setItem('auth_token', newAuthToken);
            // Update the local storage with the user's ID as well to be able to use it later
            // Note: the "me" object is an array, so we need to get the first item
            window.localStorage.setItem('user_id', res.data.me[0].id);

            // Update the React state with the user's ID, so we can use it for the limit to my account filter
            setUserId(res.data.me[0].id);

        }, (err: { message: string; }) => {
            console.error(useTranslation("ui.graphQLExplorer.statusMessages.invalidToken", locale), {err: err.message});
        });
    };

    /**
     * This function will handle the onClick event for the Run Query button.
     * We need to run the query and display the results.
     * @returns {void}
     */
    const handleRunQuery = (): void => {
        // In this version we are running the unmodified query
        // In a future version we will add the filters to the query for the limit to my account
        // and results length options

        // Set the query status to running
        setQueryStatus('running');

        // Run the query using fetch
        handleQueryWithFetch(query).then((res: any) => {
            // Update the React state with the results
            setQueryResults(res.data);

            // Set the query status to success
            setQueryStatus('success');
        }, (err: { message: string; }) => {
            // Update the React state with the error message
            setQueryError(err.message);

            // Set the query status to error
            setQueryStatus('error');
        });
    };

    // Render the component
    // This is a first draft and will be updated as we go along
    return (<>
            {isMutation && (
                <div className="relative my-4 rounded border border-red-400 bg-red-100 px-4 py-3 text-red-700"
                     role="alert">
                    <strong className="font-bold">{useTranslation("ui.graphQLExplorer.warning", locale)}</strong>
                    <span className="block sm:inline">{useTranslation("ui.graphQLExplorer.statusMessages.mutationQueryNotAllowed", locale)}</span>
                </div>)}
            {!isMutation && (
                <>
                    <div className="my-4 flex row justify-between items-center flex-wrap gap-2">
                        <div className={`flex flex-row items-center space-x-2 gap-2`}>
                            <Button
                                onClick={() => {
                                    setShowAuthToken(!showAuthToken);
                                }}
                                title={useTranslation("ui.graphQLExplorer.authToken", locale)}
                                variant="ghost"
                            >
                                <LuKeyRound/>
                            </Button>
                            <Button
                                onClick={() => {
                                    setShowQuery(!showQuery);
                                    setExplicitQuery(!explicitQuery);
                                }}
                                title={useTranslation("ui.graphQLExplorer.viewQuery", locale)}
                                variant="ghost"
                            >
                                <LuTerminal/>
                            </Button>
                        </div>

                        {!forcePresentation && (
                            <div className={`flex flex-row items-center space-x-2 gap-2`}>
                                <Button
                                    onClick={() => {
                                        setCurrentPresentation('json');
                                        setPreference('graphQLResults', 'json');
                                    }}
                                    title={useTranslation("ui.graphQLExplorer.views.json", locale)}
                                    variant='ghost'
                                    disabled={!queryResults || currentPresentation === 'json'}
                                >
                                    <LuCode/> {useTranslation("ui.graphQLExplorer.views.json", locale)}
                                </Button>
                                <Button
                                    onClick={() => {
                                        setCurrentPresentation('table');
                                        setPreference('graphQLResults', 'table');
                                    }}
                                    title={useTranslation("ui.graphQLExplorer.views.table", locale)}
                                    variant='ghost'
                                    disabled={!queryResults || currentPresentation === 'table'}
                                >
                                    <LuTable/> {useTranslation("ui.graphQLExplorer.views.table", locale)}
                                </Button>
                            </div>
                        )}

                        <Button
                            onClick={handleRunQuery}
                            title={useTranslation("ui.graphQLExplorer.runDescription", locale)}
                            variant="default"
                            disabled={queryStatus === 'running'}
                        >
                            {queryStatus === 'running' ? (
                                <><LuLoader className="animate-spin h-5 w-5 mr-3"/> {useTranslation("ui.graphQLExplorer.statusMessages.loading", locale)}</>
                            ) : (
                                useTranslation("ui.graphQLExplorer.run", locale)
                            )}
                        </Button>
                    </div>

                    {showAuthToken && (
                        <div className="my-4 mb-2 grid w-full gap-1.5">
                            <Label htmlFor="auth_token">
                                {useTranslation("ui.graphQLExplorer.authToken", locale)}
                            </Label>

                            <Textarea
                                className="mb-2 block w-full rounded-lg bg-gray-50 text-sm min-h-24 p-2.5 dark:bg-gray-700"
                                id="auth_token"
                                onChange={updateAuthTokenUI}
                                onBlur={handleAuthTokenChange}
                                title={useTranslation("ui.graphQLExplorer.authTokenDescription", locale)}
                                value={authToken}
                                required/>
                        </div>
                    )}

                    <StatusMessages queryStatus={queryStatus} queryError={queryError} locale={locale} />

                    {showQuery && (
                        <>
                            <h2 className="my-4 text-lg font-semibold text-gray-900 dark:text-white">{useTranslation("ui.graphQLExplorer.query", locale)}</h2>

                            {description && (
                                <p className="my-4 text-sm text-gray-900 dark:text-white">{description}</p>)}

                            <ScrollArea className="w-full h-48 bg-slate-50 border border-gray-300 text-gray-900 text-sm rounded-lg block p-2.5
                                dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white">
                                <pre className="">{query}</pre>
                            </ScrollArea>
                        </>
                    )}

                    {queryStatus === 'success' && (
                        <>
                            <h2 className="my-4 text-lg font-semibold text-gray-900 dark:text-white">{useTranslation("ui.graphQLExplorer.results", locale)}</h2>

                            {currentPresentation === 'json' && (
                                <JSONResults results={queryResults} locale={locale} />
                            )}

                            {currentPresentation === 'table' && (
                                <TableResults results={queryResults} locale={locale} />
                            )}
                        </>
                    )}
                </>
            )}
        </>
    );
};
````

## File: src/components/GraphQLExplorer/JSONResults.test.jsx
````javascript
import React from "react";
import { expect, it, describe } from "vitest";
import { render } from "@testing-library/react";
import { JSONResults } from "./JSONResults";

describe("JSONResults", () => {
    it("renders JSON results", () => {
        const { getByRole } = render(
            <JSONResults
                results={{ data: { test: "test" } }}
            />
        );

        expect(getByRole("log")).toBeInTheDocument();
        expect(getByRole("log")).toHaveTextContent('{ "data": { "test": "test" } }');
    });

    it("renders no results", () => {
        const { getByRole } = render(
            <JSONResults results={undefined} />
        );

        expect(getByRole("log")).toBeInTheDocument();
        expect(getByRole("log")).toHaveTextContent("No results found");
    });
});
````

## File: src/components/GraphQLExplorer/JSONResults.tsx
````typescript
import {useTranslation} from "@/lib/utils.ts";
import React from "react";
import {ScrollArea} from "@/components/ui/scroll-area"

export const JSONResults = (props: {
    results: object,
    locale?: string,
}) => {
    const {results, locale = 'en'} = props;

    return (
        <ScrollArea className="h-64 rounded-lg bg-slate-50 border border-gray-300 text-gray-900 text-sm block w-full p-2.5
                                dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white">
            <pre role="log">
                {results ? JSON.stringify(results, null, 2) : useTranslation("ui.graphQLExplorer.statusMessages.noResults", locale)}
            </pre>
        </ScrollArea>
    );
};
````

## File: src/components/GraphQLExplorer/StatusMessages.test.jsx
````javascript
import React from "react";
import { render } from "@testing-library/react";
import { StatusMessages } from "./StatusMessages";
import { expect, it, describe } from "vitest";

describe("StatusMessages", () => {
    it("renders idle message", () => {
        const {getByText} = render(<StatusMessages queryStatus="idle" />);
        expect(getByText("This will run against your account. You are responsible for the content of any queries ran on your account.", {exact: false})).toBeInTheDocument();
    });

    it("renders error message", () => {
        const { getByText } = render(
        <StatusMessages queryStatus="error" queryError="Testing Error" />
        );

        expect(getByText("Error:", {exact: false})).toBeInTheDocument();
        expect(getByText("Testing Error", {exact: false})).toBeInTheDocument();
    });

    it("renders success message", () => {
        const {getByText} = render(<StatusMessages queryStatus="success" />);
        expect(getByText("Success!", {exact: false})).toBeInTheDocument();
    });
});
````

## File: src/components/GraphQLExplorer/StatusMessages.tsx
````typescript
import {useTranslation} from "@/lib/utils.ts";
import DOMPurify from "dompurify";
import React from "react";

export const StatusMessages = (props: {
    queryStatus: 'running' | 'success' | 'error' | 'idle',
    queryError?: string,
    locale?: string,
}) => {

    const {queryStatus, queryError, locale = 'en'} = props;
    const sanitizedDisclaimerText = () => (
        DOMPurify.sanitize(
            useTranslation("ui.graphQLExplorer.statusMessages.disclaimer", locale)
        )
    );

    return (
        <>
            {(queryStatus == "idle" || !queryStatus) && (
                <div className="my-4 w-full rounded-lg p-3 text-gray-900 bg-accent-200">
                    {sanitizedDisclaimerText()}
                </div>)}

            {queryStatus == "error" && (
                <div className="my-4 w-full rounded-lg border border-red-400 bg-red-100 p-3 text-red-700">
                    <strong>{useTranslation("ui.graphQLExplorer.statusMessages.error", locale)}: </strong> {queryError}
                </div>)}

            {queryStatus == "success" && (<div
                className="my-4 w-full rounded-lg border border-green-400 bg-green-100 p-3 text-green-700">
                {useTranslation("ui.graphQLExplorer.statusMessages.success", locale)}
            </div>)}
        </>
    );
};
````

## File: src/components/GraphQLExplorer/TableResults.test.jsx
````javascript
import React from "react";
import { render } from "@testing-library/react";
import { TableResults } from "./TableResults";
import {expect, it, describe} from "vitest";

describe("TableResults", () => {
    it("renders table results", () => {
        const { getAllByRole } = render(
            <TableResults
                results={{ rows: [{ cola: "test", colb: "another cell" }, {cola: "second", colb: "fourth cell"}] }}
            />
        );

        expect(getAllByRole("cell")).toHaveLength(4);
        expect(getAllByRole("cell")[0]).toHaveTextContent("test");
        expect(getAllByRole("cell")[1]).toHaveTextContent("another cell");
        expect(getAllByRole("cell")[2]).toHaveTextContent("second");
        expect(getAllByRole("cell")[3]).toHaveTextContent("fourth cell");
    });

    it("renders no results", () => {
        const { getAllByRole, getByRole } = render(
            <TableResults results={undefined} />
        );

        expect(getAllByRole("log")).toHaveLength(1);
        expect(getByRole("log")).toHaveTextContent("No results found");
    });

    it("does not render nested objects", () => {
        const { getAllByRole, getByRole } = render(
            <TableResults
                results={{ rows: [{ cola: "test", colb: { nested: "object" } }] }}
            />
        );

        expect(getAllByRole("log")).toHaveLength(1);
        expect(getByRole("log")).toHaveTextContent("This view is not available for this query's results.");
    });
});
````

## File: src/components/GraphQLExplorer/TableResults.tsx
````typescript
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow,} from "@/components/ui/table.tsx";
import {useTranslation} from "@/lib/utils.ts";
import React, {useEffect, useState} from "react";

export const TableResults = (props: {
    results: object,
    locale?: string,
}) => {
    const {results, locale = 'en'} = props;

    const [tableColumns, setTableColumns] = useState(['']);
    const [tableRows, setTableRows] = useState([]);

    const [canRender, setCanRender] = useState(true);
    const [hasResults, setHasResults] = useState(false);

    useEffect(() => {
        if (results) {
            Object.values(results).forEach(value => {
                setTableRows(value);

                const firstRow = value[0];
                const keys = Object.keys(firstRow);
                setTableColumns(keys);

                if (keys.length > 0) {
                    setHasResults(true);
                }

                Object.values(firstRow).forEach(val => {
                    if (typeof val === 'object') {
                        setCanRender(false);
                    }
                });
            });
        }
    }, [results]);

    return (
        <div className="rounded-lg bg-slate-50 border border-gray-300 text-gray-900 text-sm block w-full min-h-64 p-2.5
                                dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white">
            {canRender && hasResults && (
                <Table>
                    <TableHeader>
                        <TableRow>
                            {tableColumns.map((col, i) => <TableHead key={i}>{col}</TableHead>)}
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {tableRows.map((row, i) => (
                            <TableRow role="row">
                                {tableColumns.map((col, x) => (
                                    <TableCell key={`row-${i}-col-${x}`} role="cell">{row[col]}</TableCell>))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>)}

            {!hasResults && canRender && (
                <pre role="log">{useTranslation("ui.graphQLExplorer.statusMessages.noResults", locale)}</pre>
            )}

            {!canRender && (
                <pre role="log">{useTranslation("ui.graphQLExplorer.statusMessages.viewUnavailable", locale)}</pre>
            )}
        </div>

    );
};
````

## File: src/components/ui/accordion.tsx
````typescript
import * as React from "react"
import * as AccordionPrimitive from "@radix-ui/react-accordion"
import { ChevronDown } from "lucide-react"

import { cn } from "@/lib/utils"

const Accordion = AccordionPrimitive.Root

const AccordionItem = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>
>(({ className, ...props }, ref) => (
  <AccordionPrimitive.Item
    ref={ref}
    className={cn("border-b", className)}
    {...props}
  />
))
AccordionItem.displayName = "AccordionItem"

const AccordionTrigger = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Header className="flex">
    <AccordionPrimitive.Trigger
      ref={ref}
      className={cn(
        "flex flex-1 items-center justify-between py-4 font-medium transition-all hover:underline [&[data-state=open]>svg]:rotate-180",
        className
      )}
      {...props}
    >
      {children}
      <ChevronDown className="h-4 w-4 shrink-0 transition-transform duration-200" />
    </AccordionPrimitive.Trigger>
  </AccordionPrimitive.Header>
))
AccordionTrigger.displayName = AccordionPrimitive.Trigger.displayName

const AccordionContent = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Content
    ref={ref}
    className="overflow-hidden text-sm transition-all data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"
    {...props}
  >
    <div className={cn("pb-4 pt-0", className)}>{children}</div>
  </AccordionPrimitive.Content>
))

AccordionContent.displayName = AccordionPrimitive.Content.displayName

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent }
````

## File: src/components/ui/button.tsx
````typescript
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
````

## File: src/components/ui/card.tsx
````typescript
import * as React from "react"

import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
````

## File: src/components/ui/input.tsx
````typescript
import * as React from "react"

import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
````

## File: src/components/ui/label.tsx
````typescript
import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const labelVariants = cva(
  "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
)

const Label = React.forwardRef<
  React.ElementRef<typeof LabelPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root> &
    VariantProps<typeof labelVariants>
>(({ className, ...props }, ref) => (
  <LabelPrimitive.Root
    ref={ref}
    className={cn(labelVariants(), className)}
    {...props}
  />
))
Label.displayName = LabelPrimitive.Root.displayName

export { Label }
````

## File: src/components/ui/popover.tsx
````typescript
import * as React from "react"
import * as PopoverPrimitive from "@radix-ui/react-popover"

import { cn } from "@/lib/utils"

const Popover = PopoverPrimitive.Root

const PopoverTrigger = PopoverPrimitive.Trigger

const PopoverContent = React.forwardRef<
  React.ElementRef<typeof PopoverPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof PopoverPrimitive.Content>
>(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
  <PopoverPrimitive.Portal>
    <PopoverPrimitive.Content
      ref={ref}
      align={align}
      sideOffset={sideOffset}
      className={cn(
        "z-50 w-72 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-popover-content-transform-origin]",
        className
      )}
      {...props}
    />
  </PopoverPrimitive.Portal>
))
PopoverContent.displayName = PopoverPrimitive.Content.displayName

export { Popover, PopoverTrigger, PopoverContent }
````

## File: src/components/ui/scroll-area.tsx
````typescript
import * as React from "react"
import * as ScrollAreaPrimitive from "@radix-ui/react-scroll-area"

import { cn } from "@/lib/utils"

const ScrollArea = React.forwardRef<
  React.ElementRef<typeof ScrollAreaPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof ScrollAreaPrimitive.Root>
>(({ className, children, ...props }, ref) => (
  <ScrollAreaPrimitive.Root
    ref={ref}
    className={cn("relative overflow-hidden", className)}
    {...props}
  >
    <ScrollAreaPrimitive.Viewport className="h-full w-full rounded-[inherit]">
      {children}
    </ScrollAreaPrimitive.Viewport>
    <ScrollBar />
    <ScrollAreaPrimitive.Corner />
  </ScrollAreaPrimitive.Root>
))
ScrollArea.displayName = ScrollAreaPrimitive.Root.displayName

const ScrollBar = React.forwardRef<
  React.ElementRef<typeof ScrollAreaPrimitive.ScrollAreaScrollbar>,
  React.ComponentPropsWithoutRef<typeof ScrollAreaPrimitive.ScrollAreaScrollbar>
>(({ className, orientation = "vertical", ...props }, ref) => (
  <ScrollAreaPrimitive.ScrollAreaScrollbar
    ref={ref}
    orientation={orientation}
    className={cn(
      "flex touch-none select-none transition-colors",
      orientation === "vertical" &&
        "h-full w-2.5 border-l border-l-transparent p-[1px]",
      orientation === "horizontal" &&
        "h-2.5 flex-col border-t border-t-transparent p-[1px]",
      className
    )}
    {...props}
  >
    <ScrollAreaPrimitive.ScrollAreaThumb className="relative flex-1 rounded-full bg-border" />
  </ScrollAreaPrimitive.ScrollAreaScrollbar>
))
ScrollBar.displayName = ScrollAreaPrimitive.ScrollAreaScrollbar.displayName

export { ScrollArea, ScrollBar }
````

## File: src/components/ui/select.tsx
````typescript
import * as React from "react"
import * as SelectPrimitive from "@radix-ui/react-select"
import { Check, ChevronDown, ChevronUp } from "lucide-react"

import { cn } from "@/lib/utils"

const Select = SelectPrimitive.Root

const SelectGroup = SelectPrimitive.Group

const SelectValue = SelectPrimitive.Value

const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background data-[placeholder]:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
      className
    )}
    {...props}
  >
    {children}
    <SelectPrimitive.Icon asChild>
      <ChevronDown className="h-4 w-4 opacity-50" />
    </SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
))
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName

const SelectScrollUpButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollUpButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollUpButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollUpButton
    ref={ref}
    className={cn(
      "flex cursor-default items-center justify-center py-1",
      className
    )}
    {...props}
  >
    <ChevronUp className="h-4 w-4" />
  </SelectPrimitive.ScrollUpButton>
))
SelectScrollUpButton.displayName = SelectPrimitive.ScrollUpButton.displayName

const SelectScrollDownButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollDownButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollDownButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollDownButton
    ref={ref}
    className={cn(
      "flex cursor-default items-center justify-center py-1",
      className
    )}
    {...props}
  >
    <ChevronDown className="h-4 w-4" />
  </SelectPrimitive.ScrollDownButton>
))
SelectScrollDownButton.displayName =
  SelectPrimitive.ScrollDownButton.displayName

const SelectContent = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Content>
>(({ className, children, position = "popper", ...props }, ref) => (
  <SelectPrimitive.Portal>
    <SelectPrimitive.Content
      ref={ref}
      className={cn(
        "relative z-50 max-h-[--radix-select-content-available-height] min-w-[8rem] overflow-y-auto overflow-x-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-select-content-transform-origin]",
        position === "popper" &&
          "data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1",
        className
      )}
      position={position}
      {...props}
    >
      <SelectScrollUpButton />
      <SelectPrimitive.Viewport
        className={cn(
          "p-1",
          position === "popper" &&
            "h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]"
        )}
      >
        {children}
      </SelectPrimitive.Viewport>
      <SelectScrollDownButton />
    </SelectPrimitive.Content>
  </SelectPrimitive.Portal>
))
SelectContent.displayName = SelectPrimitive.Content.displayName

const SelectLabel = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Label>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Label
    ref={ref}
    className={cn("py-1.5 pl-8 pr-2 text-sm font-semibold", className)}
    {...props}
  />
))
SelectLabel.displayName = SelectPrimitive.Label.displayName

const SelectItem = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <SelectPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </SelectPrimitive.ItemIndicator>
    </span>

    <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
  </SelectPrimitive.Item>
))
SelectItem.displayName = SelectPrimitive.Item.displayName

const SelectSeparator = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-muted", className)}
    {...props}
  />
))
SelectSeparator.displayName = SelectPrimitive.Separator.displayName

export {
  Select,
  SelectGroup,
  SelectValue,
  SelectTrigger,
  SelectContent,
  SelectLabel,
  SelectItem,
  SelectSeparator,
  SelectScrollUpButton,
  SelectScrollDownButton,
}
````

## File: src/components/ui/separator.tsx
````typescript
import * as React from "react"
import * as SeparatorPrimitive from "@radix-ui/react-separator"

import { cn } from "@/lib/utils"

const Separator = React.forwardRef<
  React.ElementRef<typeof SeparatorPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SeparatorPrimitive.Root>
>(
  (
    { className, orientation = "horizontal", decorative = true, ...props },
    ref
  ) => (
    <SeparatorPrimitive.Root
      ref={ref}
      decorative={decorative}
      orientation={orientation}
      className={cn(
        "shrink-0 bg-border",
        orientation === "horizontal" ? "h-[1px] w-full" : "h-full w-[1px]",
        className
      )}
      {...props}
    />
  )
)
Separator.displayName = SeparatorPrimitive.Root.displayName

export { Separator }
````

## File: src/components/ui/table.tsx
````typescript
import * as React from "react"

import { cn } from "@/lib/utils"

const Table = React.forwardRef<
  HTMLTableElement,
  React.HTMLAttributes<HTMLTableElement>
>(({ className, ...props }, ref) => (
  <div className="relative w-full overflow-auto">
    <table
      ref={ref}
      className={cn("w-full caption-bottom text-sm", className)}
      {...props}
    />
  </div>
))
Table.displayName = "Table"

const TableHeader = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <thead ref={ref} className={cn("[&_tr]:border-b", className)} {...props} />
))
TableHeader.displayName = "TableHeader"

const TableBody = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tbody
    ref={ref}
    className={cn("[&_tr:last-child]:border-0", className)}
    {...props}
  />
))
TableBody.displayName = "TableBody"

const TableFooter = React.forwardRef<
  HTMLTableSectionElement,
  React.HTMLAttributes<HTMLTableSectionElement>
>(({ className, ...props }, ref) => (
  <tfoot
    ref={ref}
    className={cn(
      "border-t bg-muted/50 font-medium [&>tr]:last:border-b-0",
      className
    )}
    {...props}
  />
))
TableFooter.displayName = "TableFooter"

const TableRow = React.forwardRef<
  HTMLTableRowElement,
  React.HTMLAttributes<HTMLTableRowElement>
>(({ className, ...props }, ref) => (
  <tr
    ref={ref}
    className={cn(
      "border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
      className
    )}
    {...props}
  />
))
TableRow.displayName = "TableRow"

const TableHead = React.forwardRef<
  HTMLTableCellElement,
  React.ThHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <th
    ref={ref}
    className={cn(
      "h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0",
      className
    )}
    {...props}
  />
))
TableHead.displayName = "TableHead"

const TableCell = React.forwardRef<
  HTMLTableCellElement,
  React.TdHTMLAttributes<HTMLTableCellElement>
>(({ className, ...props }, ref) => (
  <td
    ref={ref}
    className={cn("p-4 align-middle [&:has([role=checkbox])]:pr-0", className)}
    {...props}
  />
))
TableCell.displayName = "TableCell"

const TableCaption = React.forwardRef<
  HTMLTableCaptionElement,
  React.HTMLAttributes<HTMLTableCaptionElement>
>(({ className, ...props }, ref) => (
  <caption
    ref={ref}
    className={cn("mt-4 text-sm text-muted-foreground", className)}
    {...props}
  />
))
TableCaption.displayName = "TableCaption"

export {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
}
````

## File: src/components/ui/tabs.tsx
````typescript
import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"

import { cn } from "@/lib/utils"

const Tabs = TabsPrimitive.Root

const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground",
      className
    )}
    {...props}
  />
))
TabsList.displayName = TabsPrimitive.List.displayName

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm",
      className
    )}
    {...props}
  />
))
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
      className
    )}
    {...props}
  />
))
TabsContent.displayName = TabsPrimitive.Content.displayName

export { Tabs, TabsList, TabsTrigger, TabsContent }
````

## File: src/components/ui/textarea.tsx
````typescript
import * as React from "react"

import { cn } from "@/lib/utils"

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Textarea.displayName = "Textarea"

export { Textarea }
````

## File: src/components/APIBanner.tsx
````typescript
import React from "react";
import DOMPurify from "dompurify";

import {URLS} from "@/Consts";
import {useTokenTranslation, useTranslation} from "@/lib/utils";

export const APIBanner = (locale: any = "en") => {
    // @ts-ignore
    const bannerText: string | Node = useTokenTranslation('pages.api.disclaimerBanner.text', locale, {
        "a": (chunks: any) => {
            return `<a href=${URLS.API_DISCORD}
                   target="_blank" rel="noreferrer noopener">{chunks}</a>`
        }
    });

    const sanitizedBannerText = () => ({
        __html: DOMPurify.sanitize(bannerText)
    });

    return (
        <>
            <div className="border-l-4 border-l-yellow-600 bg-yellow-100 dark:bg-yellow-900 p-4 dark:text-white">
                <h5 className="!text-yellow-900 dark:!text-yellow-100">{
                    useTranslation('pages.api.disclaimerBanner.title', locale)
                }:</h5>
                <p dangerouslySetInnerHTML={sanitizedBannerText()}/>
            </div>
        </>
    );
}
````

## File: src/components/EditLink.tsx
````typescript
import {Components} from "@/components/index";

import {URLS} from "@/Consts";
import {getPreference, setPreference} from "@/lib/utils";
import {useEffect, useState} from "react";

import {IoSettingsOutline} from "react-icons/io5";
import {LuPencil} from "react-icons/lu";

export const EditLink = (link: any) => {
    const {text, url} = link;

    const [isDevMode, setIsDevMode] = useState(getPreference('editMode') === 'developer');
    const [editLink, setEditLink] = useState(isDevMode ? url.href.replace(URLS.GITHUB_EDIT, URLS.GITHUB_DEV) : url.href);

    useEffect(() => {
        setEditLink(isDevMode ? url.href.replace(URLS.GITHUB_EDIT, URLS.GITHUB_DEV) : url.href);
    }, [isDevMode]);


    return (
        <div className="flex items-center gap-2 ">
            <a
                href={editLink}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm no-underline font-medium text-gray-500 hover:text-gray-900
                dark:text-gray-400 dark:hover:text-white">
                <LuPencil/> {text}
            </a>

            <Components.ui.Popover>
                <Components.ui.PopoverTrigger className="bg-transparent mt-1 cursor-pointer">
                    <IoSettingsOutline/>
                </Components.ui.PopoverTrigger>
                <Components.ui.PopoverContent className="bg-gray-800 text-white">
                    <div className="flex flex-col gap-2">
                        <Components.ui.Label htmlFor="editMode">Edit Mode</Components.ui.Label>

                        <p className="text-xs ">
                            - Developer mode will open github.dev links instead of github.com links.
                            This is useful for quickly editing multiple files at once.

                            <br/>
                            <br/>

                            - Basic mode will open github.com links this is useful for quickly editing a single file.
                        </p>

                        <Components.ui.Select
                            defaultValue={getPreference('editMode')}
                            onValueChange={(value) => {
                                setPreference('editMode', value);
                                setIsDevMode(value === 'developer');
                            }}
                        >
                            <Components.ui.SelectTrigger className="w-[180px] cursor-pointer">
                                <Components.ui.SelectValue placeholder="Select edit mode"/>
                            </Components.ui.SelectTrigger>
                            <Components.ui.SelectContent className="bg-gray-700 text-white">
                                <Components.ui.SelectItem value="basic" className="cursor-pointer">Basic</Components.ui.SelectItem>
                                <Components.ui.SelectItem value="developer" className="cursor-pointer">Developer</Components.ui.SelectItem>
                            </Components.ui.SelectContent>
                        </Components.ui.Select>
                    </div>
                </Components.ui.PopoverContent>
            </Components.ui.Popover>
        </div>
    )
}
````

## File: src/components/index.tsx
````typescript
/**
 * This file is meant to be a single point to export all components from the components folder.
 * This will make it easier for community members to use the components on new pages.
 */

/**
 * shadcn/ui components
 * Most of these components have not been used on the site yet but can be added as needed.
 */
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "./ui/accordion";
// import { Alert } from "./ui/alert";
// import { AlertDialog } from "./ui/alert-dialog";
// import { AspectRatio } from "./ui/aspect-ratio";
// import { Avatar } from "./ui/avatar";
// import { Badge } from "./ui/badge";
// import { Breadcrumb } from "./ui/breadcrumb";
import { Button } from "./ui/button";
// import { Calendar } from "./ui/calendar";
import { Card } from "./ui/card";
// import { Carousel } from "./ui/carousel";
// import { Chart } from "./ui/chart";
// import { Checkbox } from "./ui/checkbox";
// import { Collapsible } from "./ui/collapsible";
// import { Command } from "./ui/command";
// import { ContextMenu } from "./ui/context-menu";
// import { DataTable } from "./ui/data-table";
// import { DatePicker } from "./ui/date-picker";
// import { Dialog } from "./ui/dialog";
// import { Drawer } from "./ui/drawer";
// import { DropdownMenu } from "./ui/dropdown-menu";
// import { Form } from "./ui/form";
// import { HoverCard } from "./ui/hover-card";
import { Input } from "./ui/input";
// import { InputOTP } from "./ui/input-otp";
import { Label } from "./ui/label";
// import { MenuBar } from "./ui/menu-bar";
// import { NavigationMenu } from "./ui/navigation-menu";
// import { Pagination } from "./ui/pagination";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
// import { Progress } from "./ui/progress";
// import { RadioGroup } from "./ui/radio-group";
// import { Resizable } from "./ui/resizable";
import { ScrollArea } from "./ui/scroll-area";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Separator } from "./ui/separator";
// import { Sheet } from "./ui/sheet";
// import { Skeleton } from "./ui/skeleton";
// import { Slider } from "./ui/slider";
// import { Sonner } from "./ui/sonner";
// import { Switch } from "./ui/switch";
import { Table } from "./ui/table";
import { Tabs } from "./ui/tabs";
import { Textarea } from "./ui/textarea";
// import { Toast } from "./ui/toast";
// import { Toggle } from "./ui/toggle";
// import { ToggleGroup } from "./ui/toggle-group";
// import { Tooltip } from "./ui/tooltip";

/** API Explorer components */
// import { ChartResults } from "./GraphQLExplorer/ChartResults" /** Internal component to GraphQLRunner, most contributors should not need this */
// import { GraphQLExplorer } from "./GraphQLExplorer/GraphQLExplorer"; /** Currently not a react component but an astro component */
import { GraphQLRunner } from "./GraphQLExplorer/GraphQLRunner";
import { JSONResults } from "./GraphQLExplorer/JSONResults";    /** Internal component to GraphQLRunner, most contributors should not need this */
import { StatusMessages } from "./GraphQLExplorer/StatusMessages"; /** Internal component to GraphQLRunner, most contributors should not need this */
import { TableResults } from "./GraphQLExplorer/TableResults"; /** Internal component to GraphQLRunner, most contributors should not need this */

/**
 * Doc Banner components
 * These are UI banner elements for the API / Librarian Guide sections
 */
import { APIBanner} from "./APIBanner";
import { LibrarianBanners } from "./LibrarianBanners";

export const Components = {
    ui: {
        Accordion,
        AccordionContent,
        AccordionItem,
        AccordionTrigger,
        Button,
        Card,
        Input,
        Label,
        Popover,
        PopoverContent,
        PopoverTrigger,
        ScrollArea,
        Select,
        SelectContent,
        SelectItem,
        SelectTrigger,
        SelectValue,
        Separator,
        Table,
        Tabs,
        Textarea,
    },
    GraphQL: {
        GraphQLRunner,
        JSONResults,
        StatusMessages,
        TableResults,
    },
    banners: {
        api: APIBanner,
        librarian: LibrarianBanners,
    }
}
````

## File: src/components/LibrarianBanners.tsx
````typescript
import React from 'react';
import DOMPurify from 'dompurify'

import {URLS} from "@/Consts";
import {useTokenTranslation, useTranslation} from '@/lib/utils';

export const LibrarianBanners = (
                                lang: any = "en"
) => {
    const {locale} = lang;

    const currentPath = window.location.pathname;
    const isStandards = currentPath.includes('/standards/');
    // const isResources = currentPath.includes('/resources/');

    // @ts-ignore
    const bannerText: string | Node = useTokenTranslation('pages.librarians.standardsBanner.text', locale, {
        "a": () => {
            return `<a href=${URLS.LIBRARIAN_DISCORD}
                                           target="_blank" rel="noreferrer noopener">{chunks}</a>`
        }
    });

    const sanitizedBannerText = () => ({
        __html: DOMPurify.sanitize(bannerText)
    });

    return (
        <>
            {isStandards && (
                <div className="border-l-4 border-l-accent-600 bg-accent-200 dark:bg-accent-950 p-4 dark:text-white">
                    <h5 className="!text-accent-900 dark:!text-accent-200">{
                        useTranslation('pages.librarians.standardsBanner.title', locale)
                    }:</h5>
                    <p dangerouslySetInnerHTML={sanitizedBannerText()}/>
                </div>
            )}
        </>
    );
}
````

## File: src/components/PageEdit.astro
````
---
const { editUrl } = Astro.props;
import { EditLink } from './EditLink';

---

<EditLink text={
        Astro.locals.t('page.editLink')
    } url={editUrl} client:only="react" />
````

## File: src/components/SocialIcons.astro
````
---
import type {Props} from '@astrojs/starlight/props';
import Default from '@astrojs/starlight/components/SocialIcons.astro';
import { URLS } from '@/Consts';

const {iconSize = '16px'} = Astro.props;
---

<!-- Unfortunately, the default Social Icons component doesn't have any support for app stores or svg icons,
so we'll need to create our own. -->

<a href={URLS.APP} rel="me" class="sl-flex" target="_blank">
    <span class="sr-only">Hardcover</span>

    <svg xmlns="http://www.w3.org/2000/svg" class="hc-icon min-w-10 transition-all duration-300 group-hover:rotate-12" fill="none"
          viewBox="0 0 1 40" role="img" aria-labelledby="svgTitle svgDescription">
        <title id="svgTitle">Hardcover</title>
        <desc id="svgDescription">Hardcover App Icon</desc>
        <path d="M12.8889 32.5982C12.666 31.7661 13.1598 30.9108 13.9919 30.6879L30.2971 26.3189C31.1292 26.096 31.9845
        26.5898 32.2075 27.4219L32.8739 29.9089C33.1711 31.0183 32.5127 32.1587 31.4033 32.456L18.1113 36.0176C15.8924
        36.6121 13.6116 35.2953 13.0171 33.0764L12.8889 32.5982Z"
              fill="#4F46E5"></path>
        <path d="M7.62314 12.946C7.05137 10.8121 8.3177 8.61876 10.4516 8.04699L16.8851 32.0571L13.0214 33.0924L7.62314
        12.946Z"
              fill="#4F46E5"></path>
        <path d="M29.3358 24.432L31.2677 23.9144L32.3584 27.985C32.6443 29.052 32.0111 30.1486 30.9442 30.4345L29.3358
        24.432Z"
              fill="#4338CA"></path>
        <path d="M26.4446 5.91475C26.1474 4.80529 25.007 4.14688 23.8975 4.44416L10.5286 8.02636C9.41911 8.32364 8.7607
        9.46403 9.05798 10.5735L14.9532 32.5748L22.6461 30.5135C23.1986 30.3654 23.5265 29.7975 23.3785 29.245C23.2304
        28.6925 23.5583 28.1245 24.1108 27.9765L29.7949 26.4535C30.9043 26.1562 31.5628 25.0158 31.2655 23.9063L26.4446
        5.91475Z"
              fill="#6366F1"></path>
        <path d="M21.0947 11.2811C21.145 10.6645 21.9408 10.4512 22.2927 10.9601L22.442 11.1761C22.5512 11.3341 22.724
        11.4365 22.9151 11.4565L23.2375 11.4902C23.838 11.553 24.0445 12.3235 23.5558 12.6781L23.2935 12.8685C23.138
        12.9813 23.0395 13.1564 23.0239 13.3479L23.0026 13.6096C22.9523 14.2262 22.1564 14.4394 21.8046 13.9306L21.6553
        13.7146C21.546 13.5566 21.3732 13.4542 21.1821 13.4342L20.8598 13.4005C20.2592 13.3377 20.0528 12.5672 20.5415
        12.2126L20.8038 12.0222C20.9593 11.9094 21.0577 11.7343 21.0734 11.5428L21.0947 11.2811Z"
              fill="#312E81"></path>
        <path d="M18.3031 16.3181C18.3533 15.7015 19.1492 15.4882 19.501 15.9971L20.5634 17.5337C20.6727 17.6917 20.8455
        17.7941 21.0366 17.8141L22.9139 18.0104C23.5144 18.0732 23.7208 18.8436 23.2321 19.1983L21.7045 20.3069C21.549
        20.4197 21.4506 20.5949 21.435 20.7863L21.2832 22.6482C21.2329 23.2649 20.4371 23.4781 20.0852 22.9692L19.0228
        21.4327C18.9136 21.2747 18.7407 21.1722 18.5497 21.1522L16.6724 20.956C16.0719 20.8932 15.8654 20.1227 16.3541
        19.7681L17.8817 18.6594C18.0372 18.5466 18.1357 18.3715 18.1513 18.18L18.3031 16.3181Z"
              fill="#312E81"></path>
        <path d="M14.9532 32.5748C14.6571 31.4697 15.3129 30.3339 16.4179 30.0378L29.8719 26.4328L30.9441 30.4345L17.4902
        34.0395C16.3851 34.3356 15.2493 33.6798 14.9532 32.5748Z"
              fill="#EEF2FF"></path>
    </svg>
</a>

<a href={URLS.APP_STORE} rel="me" class="sl-flex" target="_blank">
    <span class="sr-only">App Store</span>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" fill="currentColor"
         role="img" aria-labelledby="appleSvgTitle appleSvgDescription">
        <title id="appleSvgTitle">AppStore</title>
        <desc id="appleSvgDescription">Apple AppStore</desc>
        <path d="M400 32H48C21.5 32 0 53.5 0 80v352c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5
        48-48V80c0-26.5-21.5-48-48-48zM127 384.5c-5.5 9.6-17.8 12.8-27.3 7.3-9.6-5.5-12.8-17.8-7.3-27.3l14.3-24.7c16.1-4.9
        29.3-1.1 39.6 11.4L127 384.5zm138.9-53.9H84c-11 0-20-9-20-20s9-20 20-20h51l65.4-113.2-20.5-35.4c-5.5-9.6-2.2-21.8
        7.3-27.3 9.6-5.5 21.8-2.2 27.3 7.3l8.9 15.4 8.9-15.4c5.5-9.6 17.8-12.8 27.3-7.3 9.6 5.5 12.8 17.8 7.3 27.3l-85.8
        148.6h62.1c20.2 0 31.5 23.7 22.7 40zm98.1 0h-29l19.6 33.9c5.5 9.6 2.2 21.8-7.3 27.3-9.6 5.5-21.8
        2.2-27.3-7.3-32.9-56.9-57.5-99.7-74-128.1-16.7-29-4.8-58 7.1-67.8 13.1 22.7 32.7 56.7 58.9 102h52c11 0 20 9 20
        20 0 11.1-9 20-20 20z"></path>
    </svg>
</a>

<a href={URLS.PLAY_STORE} rel="me" class="sl-flex" target="_blank">
    <span class="sr-only">Google Play</span>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" fill="currentColor"
         role="img" aria-labelledby="googleSvgTitle googleSvgDescription">
        <title id="googleSvgTitle">Google Play</title>
        <desc id="googleSvgDescription">Google Play Store</desc>
        <path d="M420.55 301.93a24 24 0 1 1 24-24 24 24 0 0 1-24 24m-265.1 0a24 24 0 1 1 24-24 24 24 0 0 1-24
        24m273.7-144.48 47.94-83a10 10 0 1 0-17.27-10l-48.54 84.07a301.25 301.25 0 0 0-246.56 0l-48.54-84.07a10 10 0 1
        0-17.27 10l47.94 83C64.53 202.22 8.24 285.55 0 384h576c-8.24-98.45-64.54-181.78-146.85-226.55"></path>
    </svg>
</a>

<Default {...Astro.props}>
    <slot/>
</Default>

<style define:vars={{'sl-icon-size': iconSize}}>
    svg {
        &.hc-icon {
            width: calc(var(--sl-icon-size, 1em) * 1.4);
            height: calc(var(--sl-icon-size, 1em) * 1.4);
        }

        color: var(--sl-color-text-accent);
        font-size: var(--sl-icon-size, 1em);

        width: calc(var(--sl-icon-size, 1em) * 1.2);
        height: calc(var(--sl-icon-size, 1em) * 1.2);
    }

    a {
        color: var(--sl-color-text-accent);
        padding: 0.5em;
        margin: -0.5em;
    }

    a:hover {
        opacity: 0.66;
    }
</style>
````

## File: src/content/docs/api/GraphQL/Schemas/Activities.mdx
````
---
title: Activities
description: Learn about the activities schema in the Hardcover API.
category: reference
lastUpdated: 2024-10-07
layout: /src/layouts/documentation.astro
---

import { Code } from '@astrojs/starlight/components';
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## What Is an Activity?

Activities are actions that users perform on the platform.
These actions include things like liking a book, following a user, or adding a book to a shelf.
Activities are used to show what users are doing on the platform and to help users discover new content.

## Types of Activities

There are many types of activities that can be performed on the platform.
Some examples of activities include:

- A user adds a book to a shelf
- A user creates a list
- A user adds a book to a list
- A user reviews a book
- A user marks a book as read
- A user answers a prompt

See some [example payloads below](#example-payloads) for more information on the different types of activities.

## Activity Schema

The activity schema contains the following fields:

### Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>[book](../books)</td>
        <td>Relation</td>
        <td>The book details of the activity</td>
    </tr>
    <tr>
        <td>book_id</td>
        <td>String</td>
        <td>The unique identifier of the book that the activity is related to</td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>String</td>
        <td>The timestamp of when the activity occurred.</td>
    </tr>
    <tr>
        <td>[data](#example-payloads)</td>
        <td>Object</td>
        <td>The payload of the activity</td>
    </tr>
    <tr>
        <td>[event](#event-types)</td>
        <td>String</td>
        <td>The type of activity</td>
    </tr>
    <tr>
        <td>[followers](../users)</td>
        <td>Relation</td>
        <td>List of users who have followed this activity</td>
    </tr>
    <tr>
        <td>id</td>
        <td>Int</td>
        <td>The unique identifier of the activity</td>
    </tr>
    <tr>
        <td>[likes](../users)</td>
        <td>Relation</td>
        <td>List of users who have liked this activity</td>
    </tr>
    <tr>
        <td>likes_count</td>
        <td>Number</td>
        <td>The number of users who have liked this activity</td>
    </tr>
    <tr>
        <td>object_type</td>
        <td>String</td>
        <td>'Activity'</td>
    </tr>
    <tr>
        <td>[user](../users)</td>
        <td>Relation</td>
        <td>User object for the user who performed the activity</td>
    </tr>
    <tr>
        <td>user_id</td>
        <td>String</td>
        <td>The unique identifier of the user who performed the activity</td>
    </tr>
    </tbody>
</table>

### Related Schemas
These schemas use the same fields as the activities schema, and are used to help filter and query the activities.

- activity_feed
- activity_foryou_feed

### Event Types
- GoalActivity
- ListActivity
- PromptActivity
- UserBookActivity

### Example Payloads

#### User Added a Rating to a Book
<Code
    code={`
      {
        "id": 3,
        "event": "UserBookActivity",
        "data": {
          "userBook": {
            "rating": "4.5",
            "review": null,
            "statusId": 3,
            "readingFormatId": 1,
            "reviewHasSpoilers": false
          }
        },
        "book_id": 10257,
        "object_type": "Activity"
      }
`}
    lang="graphql"
    title="User Book Activity"
/>

#### User Started Reading a Book
<Code
    code={`
      {
        "id": 4,
        "event": "UserBookActivity",
        "data": {
          "userBook": {
            "rating": null,
            "review": "",
            "statusId": 1,
            "readingFormatId": 1,
            "reviewHasSpoilers": false
          }
        },
        "book_id": 10257,
        "object_type": "Activity"
      }
`}
    lang="graphql"
    title="User Started Reading"
/>

#### User Added a Review to a Book
<Code
    code={`
    {
        "id": 1234,
        "event": "UserBookActivity",
        "data": {
          "userBook": {
            "rating": "4.5",
            "review": "This is a great book!",
            "statusId": 3,
            "readingFormatId": 1,
            "reviewHasSpoilers": false
          }
        },
        "book_id": 10257,
        "object_type": "Activity"
      }
    }
`}
    lang="graphql"
    title="User Added Review"
/>

#### Goal Activity
<Code
    code={`
    {
        "data": {
          "goal": {
            "id": 12345,
            "goal": 40,
            "metric": "book",
            "endDate": "2024-12-31",
            "progress": 30,
            "startDate": "2024-01-01",
            "conditions": {},
            "description": "2024 Reading Goal",
            "percentComplete": 0.75,
            "privacySettingId": 1
          }
        },
        "event": "GoalActivity",
        "object_type": "Activity"
     },
    }
`}
    lang="graphql"
    title="Goal Activity"
/>

#### List Activity
<Code
    code={`
      {
        "data": {
          "list": {
            "id": 1234,
            "url": null,
            "name": "Owned",
            "path": "@user/lists/owned",
            "ranked": false,
            "featured": false,
            "listBooks": [
              {
                "book": ... See Book schema,
                "position": null,
                "updatedAt": "2024-09-23T23:58:14.027Z"
              }
            ],
            "updatedAt": "2024-09-23T23:58:14.040Z",
            "booksCount": 1,
            "description": "Any editions of books you've marked as 'owned' will show up in this list.",
            "followersCount": 0,
            "privacySettingId": 1
          }
        },
      },
      "event": "ListActivity",
      "object_type": "Activity",
      "book_id": 1108457
    }
}`}
    lang="graphql"
    title="List Activity"
/>

#### Prompt Activity
<Code
    code={`
    {
        "data": {
          "prompt": {
            "id": 1,
            "slug": "what-are-your-favorite-books-of-all-time",
            "user": {
                ... See User schema
            },
            "answers": [{
                "book": ... See Book schema
              }
            ],
            "question": "What are your favorite books of all time?",
            "description": "What are some of your favorites? These can be from any time of your life."
          }
        },
        "event": "PromptActivity",
        "object_type": "Activity",
        "book_id": 370893
    }
`}
    lang="graphql"
    title="Prompt Activity"
/>

## Example Queries

Let's take a look at some example queries that you can use to interact with the activities' schema.

### Get My Activities
<GraphQLExplorer query={`
{
    activities(where: {user_id: {_eq: ##USER_ID##}}, limit: 10) {
        event
        likes_count
        book_id
        created_at
    }
}
`} description={`
    This query will return a list of 10 activities that the current user has performed.
`}
    title="My Activities"
    presentation='table'
/>

### Get Activities for a Specific Book
<GraphQLExplorer query={`
{
      activities(
            order_by: {created_at: desc}
            where: {book_id: {_eq: 10257}, event: {_eq: "UserBookActivity"}}
            limit: 10
      ) {
            data
            event
            object_type
            book_id
      }
}
`} description={`
    This query will return a list of 10 activities that have occurred for a specific book.
`}
    title="Book Specific Activities"
/>
````

## File: src/content/docs/api/GraphQL/Schemas/Authors.mdx
````
---
title: Authors
category: reference
lastUpdated: 2025-08-14
layout: /src/layouts/documentation.astro
---


import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Author Schema

The author schema contains the following fields:

### Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>alternate_names</td>
        <td>Array of Strings</td>
        <td>Alternate names for the author</td>
    </tr>
    <tr>
        <td>bio</td>
        <td>String</td>
        <td>The biography of the author</td>
    </tr>
    <tr>
        <td>books_count</td>
        <td>Int</td>
        <td>The number of books the author has contributed to</td>
    </tr>
    <tr>
        <td>born_date</td>
        <td>Date</td>
        <td>The date the author was born</td>
    </tr>
    <tr>
        <td>born_year</td>
        <td>Int</td>
        <td>The year the author was born</td>
    </tr>
    <tr>
        <td>cached_image</td>
        <td>Object</td>
        <td>Metadata for the authors image. This includes the image id, url, primary color, width, and height</td>
    </tr>
    <tr>
        <td>contributions</td>
        <td>[Contribution](../contributions)</td>
        <td>The contributions the author is listed on</td>
    </tr>
    <tr>
        <td>death_date</td>
        <td>Date</td>
        <td>The date the author died</td>
    </tr>
    <tr>
        <td>death_year</td>
        <td>Int</td>
        <td>The year the author died</td>
    </tr>
    <tr>
        <td>id</td>
        <td>Int</td>
        <td>The unique identifier of the author</td>
    </tr>
    <tr>
        <td>identifiers</td>
        <td>Array of objects</td>
        <td>IDs for the author on other platforms</td>
    </tr>
    <tr>
        <td>is_bipoc</td>
        <td>Boolean</td>
        <td>Whether the author is Black, Indigenous, or a Person of Color</td>
    </tr>
    <tr>
        <td>is_lgbtq</td>
        <td>Boolean</td>
        <td>Whether the author is LGBTQ+</td>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>The name of the author</td>
    </tr>
    <tr>
        <td>slug</td>
        <td>String</td>
        <td>The Hardcover URL slug</td>
    </tr>
    </tbody>
</table>

## Example Queries

### Get All Authors
<GraphQLExplorer query={`
query {
    authors(limit: 10) {
        id,
        name
    }
}
`}
    title="All Authors"
    presentation="table"/>

### Get an Author by ID

<GraphQLExplorer query={`
query {
    authors(where: {id: {_eq: 80626}}, limit: 1) {
        id,
        name
    }
}
`}
    title="Author by ID"
    presentation="table"/>
    
### Get an Author by Name

<GraphQLExplorer query={`
query {
    authors(where: {name: {_eq: "J.K. Rowling"}}) {
        books_count
        identifiers
        name
    }
}
`} 
    title="Author by Name"
    presentation='json'
    forcePresentation
/>

### Get Books by an Author
<GraphQLExplorer query={`
query GetBooksByAuthor {
    authors(where: {name: {_eq: "Dan Wells"}}) {
        books_count
        name
        contributions(where: {contributable_type: {_eq: "Book"}}) {
            book {
                title
            }
        }
    }
}
`}
    description={`
    Returns a list of books authored by Dan Wells.
    `}
    title="Books by Author"
    presentation='json'
    forcePresentation/>
````

## File: src/content/docs/api/GraphQL/Schemas/Books.mdx
````
---
title: Books
category: reference
lastUpdated: 2025-08-15
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>compilation</td>
        <td>bool</td>
        <td></td>
    </tr>
    <tr>
        <td>release_year</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>rating</td>
        <td>float</td>
        <td></td>
    </tr>
    <tr>
        <td>pages</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>users_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>lists_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>ratings_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>reviews_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>author_names</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>cover_color</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>genres</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>moods</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>content_warnings</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>tags</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>series_names</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>has_audiobook</td>
        <td>bool</td>
        <td></td>
    </tr>
    <tr>
        <td>has_ebook</td>
        <td>bool</td>
        <td></td>
    </tr>
    <tr>
        <td>contribution_types</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>slug</td>
        <td>string</td>
        <td></td>
    </tr>
    <tr>
        <td>title</td>
        <td>string</td>
        <td></td>
    </tr>
    <tr>
        <td>description</td>
        <td>string</td>
        <td></td>
    </tr>
    <tr>
        <td>subtitle</td>
        <td>string</td>
        <td></td>
    </tr>
    <tr>
        <td>release_date</td>
        <td>date</td>
        <td></td>
    </tr>
    <tr>
        <td>audio_seconds</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>users_read_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>prompts_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>activities_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>release_date_i</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>featured_book_series</td>
        <td>book_series</td>
        <td></td>
    </tr>
    <tr>
        <td>featured_series_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>alternative_titles</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>isbns</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>contributions</td>
        <td>contributions[]</td>
        <td></td>
    </tr>
    <tr>
        <td>image</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>book_category_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>book_characters</td>
        <td>[Characters](../characters)</td>
        <td></td>
    </tr>
    <tr>
        <td>book_mappings</td>
        <td>book_mappings[]</td>
        <td></td>
    </tr>
    <tr>
        <td>book_series</td>
        <td>book_series[]</td>
        <td></td>
    </tr>
    <tr>
        <td>book_status</td>
        <td>book_statuses</td>
        <td></td>
    </tr>
    <tr>
        <td>canonical</td>
        <td>Books</td>
        <td></td>
    </tr>
    <tr>
        <td>canonical_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>timestamp</td>
        <td></td>
    </tr>
    <tr>
        <td>created_by_user_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>default_audio_edition</td>
        <td>[Editions](../editions)</td>
        <td></td>
    </tr>
    <tr>
        <td>default_audio_edition_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>default_cover_edition</td>
        <td>[Editions](../editions)</td>
        <td></td>
    </tr>
    <tr>
        <td>default_cover_edition_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>default_ebook_edition</td>
        <td>[Editions](../editions)</td>
        <td></td>
    </tr>
    <tr>
        <td>default_ebook_edition_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>default_physical_edition</td>
        <td>[Editions](../editions)</td>
        <td></td>
    </tr>
    <tr>
        <td>default_physical_edition_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>dto</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>dto_combined</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>dto_external</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>editions</td>
        <td>[Editions](../editions)</td>
        <td></td>
    </tr>
    <tr>
        <td>editions_count</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>header_image_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>headline</td>
        <td>string</td>
        <td></td>
    </tr>
    <tr>
        <td>id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>image</td>
        <td>images[]</td>
        <td></td>
    </tr>
    <tr>
        <td>import_platform_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>journals_count</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>links</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>list_books</td>
        <td>list_books[]</td>
        <td></td>
    </tr>
    <tr>
        <td>literary_type_id</td>
        <td>int</td>
        <td></td>
    </tr>
    <tr>
        <td>locked</td>
        <td>bool</td>
        <td></td>
    </tr>
    <tr>
        <td>prompt_answers</td>
        <td>prompt_answers[]</td>
        <td></td>
    </tr>
    <tr>
        <td>prompt_summaries</td>
        <td>prompt_books_summary[]</td>
        <td></td>
    </tr>
    <tr>
        <td>ratings_distribution</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>recommendations</td>
        <td>recommendations[]</td>
        <td></td>
    </tr>
    <tr>
        <td>state</td>
        <td>string</td>
        <td></td>
    </tr>
    <tr>
        <td>taggable_counts</td>
        <td>taggable_counts[]</td>
        <td></td>
    </tr>
    <tr>
        <td>taggings</td>
        <td>taggings[]</td>
        <td></td>
    </tr>
    <tr>
        <td>updated_at</td>
        <td>timestamptz</td>
        <td></td>
    </tr>
    <tr>
        <td>user_added</td>
        <td>bool</td>
        <td></td>
    </tr>
    <tr>
        <td>user_books</td>
        <td>user_books[]</td>
        <td></td>
    </tr>
    </tbody>
</table>


# User Book Statuses

<table>
    <thead>
        <tr>
            <th>Status</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Want to Read</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Currently Reading</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Read</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Paused</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Did Not Finished</td>
        </tr>
        <tr>
            <td>6</td>
            <td>Ignored</td>
        </tr>
    </tbody>
</table>

## Get a List of Books in a User’s Library

<GraphQLExplorer query={`
{
      user_books(
            where: {
                user_id: {_eq: ##USER_ID##}
            },
            distinct_on: book_id
            limit: 5
            offset: 0
      ) {
        book {
              title
              pages
              release_date
        }
      }
}
`} description={`
    This query will return a list of books that the user has added to their collection.
`}
    title="User Books"
    presentation='json'
    forcePresentation
/>

## Get a List of Books by a Specific Author

<GraphQLExplorer query={`
query BooksByUserCount {
      books(
            where: {
                contributions: {
                    author: {
                        name: {_eq: "Brandon Sanderson"}
                    }
                }
            }
            limit: 10
            order_by: {users_count: desc}
      ) {
            pages
            title
            id
      }
}
`} description={`
    This query will return a list of the top 10 books by the author Brandon Sanderson, ordered by the number of users who have added the book to their collection.
`}
    title="Books by User Count"
    presentation='table'
/>

## Getting All Editions of a Book
<GraphQLExplorer query={`
query GetEditionsFromTitle {
    editions(where: {title: {_eq: "Oathbringer"}}) {
        id
        title
        edition_format
        pages
        release_date
        isbn_10
        isbn_13
        publisher {
            name
        }
    }
}
`} description='Get all of the editions for the specific title of `Oathbringer`'
    title="Editions from Title"
    presentation='json'
    forcePresentation
/>

## Create a New Book
<GraphQLExplorer query={`
mutation {
      createBook(input: {
            title: "My First Book",
            pages: 300,
            release_date: "2024-09-07"
            description: "This is my first book."
        }) {
        book {
              title
              pages
              release_date
              description
        }
      }
}
`} description={`
    This mutation will create a new book with the specified title, number of pages, release date, and description.
`}
    title="Create Book"
/>
````

## File: src/content/docs/api/GraphQL/Schemas/Characters.mdx
````
---
title: Characters
category: reference
lastUpdated: 2025-04-28 14:30:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## What Is a Character?

Characters are fictional individuals that appear in books. The characters schema in Hardcover allows you to track and explore characters across different books, including information about their attributes, the books they appear in, and their creators.

## Character Schema

The character schema contains the following fields:

### Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>Int</td>
        <td>The unique identifier of the character</td>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>The name of the character</td>
    </tr>
    <tr>
        <td>biography</td>
        <td>String</td>
        <td>A text description of the character's background and story</td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>DateTime</td>
        <td>The timestamp when the character was created in the system</td>
    </tr>
    <tr>
        <td>updated_at</td>
        <td>DateTime</td>
        <td>The timestamp when the character was last updated</td>
    </tr>
    <tr>
        <td>gender_id</td>
        <td>Int</td>
        <td>Reference to the character's gender</td>
    </tr>
    <tr>
        <td>has_disability</td>
        <td>Boolean</td>
        <td>Indicates if the character has a disability</td>
    </tr>
    <tr>
        <td>is_lgbtq</td>
        <td>Boolean</td>
        <td>Indicates if the character identifies as LGBTQ+</td>
    </tr>
    <tr>
        <td>is_poc</td>
        <td>Boolean</td>
        <td>Indicates if the character is a person of color</td>
    </tr>
    <tr>
        <td>image_id</td>
        <td>String</td>
        <td>Reference to an image associated with the character</td>
    </tr>
    <tr>
        <td>slug</td>
        <td>String</td>
        <td>URL-friendly version of the character's name</td>
    </tr>
    <tr>
        <td>state</td>
        <td>String</td>
        <td>The current state of the character record (e.g., "active")</td>
    </tr>
    <tr>
        <td>object_type</td>
        <td>String</td>
        <td>The type of object, typically "Character"</td>
    </tr>
    <tr>
        <td>user_id</td>
        <td>String</td>
        <td>The ID of the user who created or owns this character record</td>
    </tr>
    </tbody>
</table>

## Example Queries

### Get All Characters
<GraphQLExplorer query={`
query {
    characters(limit: 10) {
        id,
        name
    }
}
`}
    title="All Characters"
    presentation="table"
/>

### Get a Character by ID

<GraphQLExplorer query={`
query {
    characters(where: {id: {_eq: "1"}}, limit: 1) {
        id,
        name
    }
}
`}
    title="Character by ID"
    presentation="table"
/>

### Get a Character by Name

<GraphQLExplorer query={`
query {
    characters(where: {name: {_eq: "Harry Potter"}}) {
        biography
        slug
        state
        name
    }
}
`}
    title="Character by Name"
    presentation='json'
    forcePresentation
/>

### Get Books Featuring a Character
<GraphQLExplorer query={`
query GetCharacterBooks {
    characters(where: {name: {_eq: "Harry Potter"}}) {
        name
        book_characters {
            book {
                title
            }
        }
        contributions {
            author {
                name
            }
        }
    }
}
`} 
    title="Books Featuring Character"
    presentation='json'
    forcePresentation
/>
````

## File: src/content/docs/api/GraphQL/Schemas/Contributions.mdx
````
---
title: Contributions
category: reference
lastUpdated: 2025-07-25 00:00:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import {Aside} from "@astrojs/starlight/components";

# What Is a Contribution?

A Contribution in Hardcover represents the relationship between an author and a book or edition, along with the specific role the author played. This flexible system allows for various types of contributions including writing, illustration, translation, editing, and more, providing detailed credit information for all contributors to a work.

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>bigint</td>
        <td>Unique identifier for the contribution</td>
    </tr>
    <tr>
        <td>author_id</td>
        <td>int</td>
        <td>ID of the contributing author</td>
    </tr>
    <tr>
        <td>contributable_id</td>
        <td>int</td>
        <td>ID of the item being contributed to (book or edition)</td>
    </tr>
    <tr>
        <td>contributable_type</td>
        <td>string</td>
        <td>Type of item: "Book" or "Edition"</td>
    </tr>
    <tr>
        <td>contribution</td>
        <td>string</td>
        <td>Role or type of contribution (Author, Illustrator, Translator, etc.)</td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>timestamp</td>
        <td>When the contribution was recorded</td>
    </tr>
    <tr>
        <td>updated_at</td>
        <td>timestamp</td>
        <td>When the contribution was last updated</td>
    </tr>
    <tr>
        <td>author</td>
        <td>Author</td>
        <td>Author object with complete information</td>
    </tr>
    <tr>
        <td>book</td>
        <td>Book</td>
        <td>Book object (when contributable_type is "Book")</td>
    </tr>
    </tbody>
</table>

# Common Contribution Types

<table>
    <thead>
    <tr>
        <th>Contribution Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>Author</td>
        <td>Primary writer of the book</td>
    </tr>
    <tr>
        <td>Illustrator</td>
        <td>Created illustrations or artwork</td>
    </tr>
    <tr>
        <td>Translator</td>
        <td>Translated the work to another language</td>
    </tr>
    <tr>
        <td>Editor</td>
        <td>Edited or compiled the work</td>
    </tr>
    <tr>
        <td>Narrator</td>
        <td>Narrated the audiobook version</td>
    </tr>
    <tr>
        <td>Foreword</td>
        <td>Wrote the foreword or introduction</td>
    </tr>
    <tr>
        <td>Afterword</td>
        <td>Wrote the afterword or conclusion</td>
    </tr>
    <tr>
        <td>Cover Artist</td>
        <td>Created the cover art or design</td>
    </tr>
    </tbody>
</table>

# Related Schemas

- [Authors](/api/graphql/schemas/authors) - The contributors to books
- [Books](/api/graphql/schemas/books) - Works that receive contributions
- [Editions](/api/graphql/schemas/editions) - Specific editions with unique contributions

# Example Queries

## Get Book Contributors

Retrieve all contributors for a specific book with their roles:

<GraphQLExplorer query={`
query GetBookContributors {
    books(where: {id: {_eq: 328491}}) {
        id
        title
        contributions {
            id
            contribution
            author {
                id
                name
                bio
            }
        }
    }
}
`} title="Book Contributors"/>

## Get Author's Contributions

Find all works an author has contributed to with their roles:

<GraphQLExplorer query={`
query GetAuthorContributions {
    contributions(
        where: {author_id: {_eq: 80626}}
        order_by: {created_at: desc}
    ) {
        id
        contribution
        contributable_type
        book {
            id
            title
            release_year
            rating
        }
        created_at
    }
}
`} title="Author Contributions"/>

## Find Books by Illustrator

Search for books that have illustrators and display their names:

<GraphQLExplorer query={`
query FindBooksByContributor {
    contributions(
        where: {
            contribution: {_eq: "Illustrator"}
            book: {id: {_is_null: false}}
        }
        order_by: {created_at: desc}
        limit: 10
    ) {
        id
        contribution
        author {
            name
        }
        book {
            id
            title
            rating
            release_year
        }
    }
}
`} title="Books by Contributor Type"/>

## Find Authors With Multiple Roles

Discover authors who have contributed to books in different roles (e.g., as both author and illustrator):

<Aside type="note">
    This query finds authors who have contributions with roles other than "Author", helping identify versatile creators who write, illustrate, translate, or contribute in multiple ways.
</Aside>

<GraphQLExplorer query={`
query AuthorMultipleRoles {
    authors(
        where: {
            contributions_aggregate: {
                count: {
                    predicate: {_gt: 0},
                    filter: {contribution: {_neq: "Author"}}
                }
            }
        }
    ) {
        id
        name
        contributions_aggregate(
            distinct_on: contribution
        ) {
            nodes {
                contribution
            }
        }
        contributions(
            distinct_on: contribution
            limit: 5
        ) {
            contribution
        }
    }
}
`} title="Authors With Multiple Roles"/>

## Edition-Specific Contributors

Find contributors specific to particular editions:

<GraphQLExplorer query={`
query EditionContributors {
    contributions(
        where: {contributable_type: {_eq: "Edition"}}
        order_by: {created_at: desc}
        limit: 20
    ) {
        id
        contribution
        author {
            name
        }
        # The contributable_id field references the edition ID
        # You can join this with editions table to get edition details
        contributable_id
        created_at
    }
}
`} title="Edition-Specific Contributors"/>

<Aside type="note">
    Edition-specific contributions are used when a contribution applies only to a particular edition, not the work as a whole. Common examples include:
    - Translators for translated editions
    - Narrators for audiobook editions
    - Cover artists for specific print runs
    - Editors for revised editions
    
    The original author is typically credited at the book level, while edition-specific contributors are linked to individual editions.
</Aside>
````

## File: src/content/docs/api/GraphQL/Schemas/Countries.mdx
````
---
title: Countries
category: reference
lastUpdated: 2025-07-25 00:00:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import {Aside} from "@astrojs/starlight/components";

# What Is a Country?

A Country in Hardcover represents the country of publication for books and editions. This information helps users discover literature from specific regions, understand publishing markets, and explore global literary traditions. Countries use standardized codes for consistency and integration.

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>bigint</td>
        <td>Unique identifier for the country</td>
    </tr>
    <tr>
        <td>name</td>
        <td>string</td>
        <td>Full name of the country</td>
    </tr>
    <tr>
        <td>code2</td>
        <td>string</td>
        <td>Two-letter ISO 3166-1 alpha-2 country code</td>
    </tr>
    <tr>
        <td>code3</td>
        <td>string</td>
        <td>Three-letter ISO 3166-1 alpha-3 country code</td>
    </tr>
    <tr>
        <td>iso_3166</td>
        <td>string</td>
        <td>ISO 3166 standard code</td>
    </tr>
    <tr>
        <td>phone_code</td>
        <td>string</td>
        <td>International dialing code</td>
    </tr>
    <tr>
        <td>region</td>
        <td>string</td>
        <td>Geographic region (e.g., Europe, Asia)</td>
    </tr>
    <tr>
        <td>region_code</td>
        <td>string</td>
        <td>Numeric code for the region</td>
    </tr>
    <tr>
        <td>sub_region</td>
        <td>string</td>
        <td>Geographic sub-region (e.g., Western Europe)</td>
    </tr>
    <tr>
        <td>sub_region_code</td>
        <td>string</td>
        <td>Numeric code for the sub-region</td>
    </tr>
    <tr>
        <td>intermediate_region</td>
        <td>string</td>
        <td>Intermediate geographic classification</td>
    </tr>
    <tr>
        <td>intermediate_region_code</td>
        <td>string</td>
        <td>Code for intermediate region</td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>timestamp</td>
        <td>When the country was added to the system</td>
    </tr>
    <tr>
        <td>updated_at</td>
        <td>timestamp</td>
        <td>When the country record was last updated</td>
    </tr>
    <tr>
        <td>editions</td>
        <td>Edition[]</td>
        <td>Book editions published in this country</td>
    </tr>
    </tbody>
</table>

# Country Code Standards

<table>
    <thead>
    <tr>
        <th>Standard</th>
        <th>Example</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>ISO 3166-1 alpha-2</td>
        <td>US, GB, FR</td>
        <td>Two-letter country codes</td>
    </tr>
    <tr>
        <td>ISO 3166-1 alpha-3</td>
        <td>USA, GBR, FRA</td>
        <td>Three-letter country codes</td>
    </tr>
    </tbody>
</table>

<Aside type="caution">
    **Known Issue**: The `code2` and `code3` fields are currently returned in lowercase format, but according to ISO 3166-1 standards, these codes should be uppercase. This is a known bug that will be addressed in a future update.
</Aside>

# Major Publishing Countries

<table>
    <thead>
    <tr>
        <th>Country</th>
        <th>Code2</th>
        <th>Code3</th>
        <th>Publishing Notes</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>United States</td>
        <td>US</td>
        <td>USA</td>
        <td>Major English-language publishing market</td>
    </tr>
    <tr>
        <td>United Kingdom</td>
        <td>GB</td>
        <td>GBR</td>
        <td>Historical publishing center, English literature</td>
    </tr>
    <tr>
        <td>Germany</td>
        <td>DE</td>
        <td>DEU</td>
        <td>Large European publishing market</td>
    </tr>
    <tr>
        <td>France</td>
        <td>FR</td>
        <td>FRA</td>
        <td>French literature and philosophy</td>
    </tr>
    <tr>
        <td>Japan</td>
        <td>JP</td>
        <td>JPN</td>
        <td>Manga, light novels, Japanese literature</td>
    </tr>
    </tbody>
</table>

# Related Schemas

- [Editions](/api/graphql/schemas/editions) - Book editions with country of publication
- [Publishers](/api/graphql/schemas/publishers) - Publishers based in different countries
- [Authors](/api/graphql/schemas/authors) - Authors from various countries

# Example Queries

## Get All Countries

Retrieve all available countries:

<GraphQLExplorer query={`
query AllCountries {
    countries(
        order_by: {name: asc}
    ) {
        id
        name
        code2
        code3
    }
}
`} title="All Countries"/>

## Find Country by Code

Look up a country using its ISO code:

<GraphQLExplorer query={`
query CountryByCode {
    countries(
        where: {code2: {_eq: "US"}}
    ) {
        id
        name
        code2
        code3
        created_at
    }
}
`}
    title="Country by Code"/>

## Search Countries by Name

Find countries by partial name match:

<GraphQLExplorer query={`
query SearchCountries {
    countries(
        where: {name: {_eq: "United States"}}
    ) {
        id
        name
        code2
        code3
    }
}
`} title="Search Countries"/>

## Get European Countries

Find European countries:

<GraphQLExplorer query={`
query EuropeanCountries {
    countries(
        where: {
            code2: {_in: ["GB", "FR", "DE", "IT", "ES", "NL", "SE", "NO", "DK", "CH"]}
        }
        order_by: {name: asc}
    ) {
        id
        name
        code2
        code3
        region
        sub_region
    }
}
`} title="European Countries"/>

## Get Countries With Editions

Find countries that have published editions:

<GraphQLExplorer query={`
query CountriesWithEditions {
    countries(
        order_by: {name: asc}
        limit: 20
    ) {
        id
        name
        code2
        code3
        editions(limit: 3) {
            id
            title
            release_year
        }
    }
}
`} title="Countries With Editions"/>

## Get Publishing Countries

Find countries that have published editions:

<GraphQLExplorer query={`
query PublishingCountries {
    countries(
        order_by: {name: asc}
        limit: 10
    ) {
        id
        name
        code2
        code3
        editions(limit: 5) {
            id
            title
            release_year
        }
    }
}
`} title="Publishing Countries"/>

## Get Recent Country Additions

Find recently added countries:

<GraphQLExplorer query={`
query RecentCountries {
    countries(
        order_by: {created_at: desc}
        limit: 10
    ) {
        id
        name
        code2
        code3
        created_at
        updated_at
    }
}
`} title="Recent Countries"/>

<Aside type="note">
    Country codes follow international standards (ISO 3166-1) to ensure consistency across different systems and applications. This enables integration with other services and databases.
</Aside>

## Best Practices for Working With Countries

1. **Use Standard Codes**: Prefer ISO codes over country names for programmatic use
2. **Consider Historical Changes**: Some countries may have changed names or codes over time
3. **Regional Variations**: Be aware of regional publishing differences within countries
4. **Fallback Handling**: Always have fallback logic for unknown country codes
5. **Publishing Context**: Remember this represents publication country, not author nationality
````

## File: src/content/docs/api/GraphQL/Schemas/Editions.mdx
````
---
title: Editions
category: reference
lastUpdated: 2025-06-24 20:42:24
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import {Aside} from "@astrojs/starlight/components";

# What Is an Edition?

An Edition in Hardcover represents a specific published version of a book. While a book is the conceptual work (e.g., "Pride and Prejudice"), an edition is a particular physical or digital manifestation with specific attributes like ISBN, publisher, format, and release date. Multiple editions of the same book may exist with different publishers, languages, formats, or cover art.

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>int</td>
        <td>Unique identifier for the edition</td>
    </tr>
    <tr>
        <td>title</td>
        <td>string</td>
        <td>Title of this edition</td>
    </tr>
    <tr>
        <td>subtitle</td>
        <td>string</td>
        <td>Subtitle of this edition</td>
    </tr>
    <tr>
        <td>isbn_10</td>
        <td>string</td>
        <td>10-digit ISBN</td>
    </tr>
    <tr>
        <td>isbn_13</td>
        <td>string</td>
        <td>13-digit ISBN</td>
    </tr>
    <tr>
        <td>asin</td>
        <td>string</td>
        <td>Amazon Standard Identification Number</td>
    </tr>
    <tr>
        <td>pages</td>
        <td>int</td>
        <td>Number of pages</td>
    </tr>
    <tr>
        <td>audio_seconds</td>
        <td>int</td>
        <td>Duration in seconds (for audiobooks)</td>
    </tr>
    <tr>
        <td>release_date</td>
        <td>date</td>
        <td>Full release date</td>
    </tr>
    <tr>
        <td>release_year</td>
        <td>int</td>
        <td>Year of release</td>
    </tr>
    <tr>
        <td>physical_format</td>
        <td>string</td>
        <td>Physical format (hardcover, paperback, etc.)</td>
    </tr>
    <tr>
        <td>edition_format</td>
        <td>string</td>
        <td>Edition format information</td>
    </tr>
    <tr>
        <td>edition_information</td>
        <td>string</td>
        <td>Additional edition details</td>
    </tr>
    <tr>
        <td>description</td>
        <td>string</td>
        <td>Description of this edition</td>
    </tr>
    <tr>
        <td>book_id</td>
        <td>int</td>
        <td>ID of the parent book</td>
    </tr>
    <tr>
        <td>publisher_id</td>
        <td>int</td>
        <td>ID of the publisher</td>
    </tr>
    <tr>
        <td>language_id</td>
        <td>int</td>
        <td>ID of the language</td>
    </tr>
    <tr>
        <td>country_id</td>
        <td>int</td>
        <td>ID of the country of publication</td>
    </tr>
    <tr>
        <td>reading_format_id</td>
        <td>int</td>
        <td>ID of the reading format</td>
    </tr>
    <tr>
        <td>image_id</td>
        <td>int</td>
        <td>ID of the cover image</td>
    </tr>
    <tr>
        <td>rating</td>
        <td>numeric</td>
        <td>Average rating for this edition</td>
    </tr>
    <tr>
        <td>users_count</td>
        <td>int</td>
        <td>Number of users who have this edition</td>
    </tr>
    <tr>
        <td>users_read_count</td>
        <td>int</td>
        <td>Number of users who have read this edition</td>
    </tr>
    <tr>
        <td>lists_count</td>
        <td>int</td>
        <td>Number of lists containing this edition</td>
    </tr>
    <tr>
        <td>locked</td>
        <td>bool</td>
        <td>Whether the edition is locked from editing</td>
    </tr>
    <tr>
        <td>state</td>
        <td>string</td>
        <td>Current state of the edition record</td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>timestamp</td>
        <td>When the edition was created</td>
    </tr>
    <tr>
        <td>updated_at</td>
        <td>timestamp</td>
        <td>When the edition was last updated</td>
    </tr>
    <tr>
        <td>book</td>
        <td>Book</td>
        <td>Parent book object</td>
    </tr>
    <tr>
        <td>publisher</td>
        <td>Publisher</td>
        <td>Publisher object</td>
    </tr>
    <tr>
        <td>language</td>
        <td>Language</td>
        <td>Language object</td>
    </tr>
    <tr>
        <td>country</td>
        <td>Country</td>
        <td>Country object</td>
    </tr>
    <tr>
        <td>reading_format</td>
        <td>ReadingFormat</td>
        <td>Reading format object</td>
    </tr>
    <tr>
        <td>image</td>
        <td>Image</td>
        <td>Cover image object</td>
    </tr>
    <tr>
        <td>contributions</td>
        <td>Contribution[]</td>
        <td>Array of contributor relationships</td>
    </tr>
    </tbody>
</table>

# Related Schemas

- [Books](/api/graphql/schemas/books) - Parent book for editions
- [Publishers](/api/graphql/schemas/publishers) - Publishers of editions
- [Languages](/api/graphql/schemas/languages) - Edition languages
- [Authors](/api/graphql/schemas/authors) - Authors via contributions

# Example Queries

## Get Edition Details by ISBN

Retrieve detailed information about a specific edition by ISBN.

<GraphQLExplorer query={`
query GetEditionByISBN {
    editions(where: {isbn_13: {_eq: "9780547928227"}}) {
        id
        title
        subtitle
        isbn_13
        isbn_10
        asin
        pages
        release_date
        physical_format
        publisher {
            name
        }
        book {
            id
            title
            rating
            contributions {
                author {
                    name
                }
            }
        }
        language {
            language
        }
        reading_format {
            format
        }
    }
}
`} title="Edition Details by ISBN"/>

## Get All Editions of a Book

Find all editions of a specific book, showing different formats and publishers.

<Aside type="note">
    Different editions may have varying page counts, publishers, and formats. This helps readers find their preferred edition.
</Aside>

<GraphQLExplorer query={`
query GetBookEditions {
    editions(
        where: {book_id: {_eq: 328491}}
        order_by: {release_date: desc}
    ) {
        id
        title
        isbn_13
        pages
        release_date
        physical_format
        publisher {
            name
        }
        language {
            language
        }
        reading_format {
            format
        }
        users_count
        rating
    }
}
`} title="Book Editions"/>

## Find Editions by Publisher

Get recent editions from a specific publisher.

<GraphQLExplorer query={`
query GetPublisherEditions {
    editions(
        where: {publisher_id: {_eq: 1}}
        order_by: {release_date: desc}
        limit: 10
    ) {
        id
        title
        isbn_13
        release_date
        physical_format
        book {
            title
            rating
            contributions {
                author {
                    name
                }
            }
        }
    }
}
`} title="Publisher Editions"/>

## Search Editions by Format

Find audiobook editions with specific criteria.

<GraphQLExplorer query={`
query GetAudiobookEditions {
    editions(
        where: {reading_format_id: {_eq: 2}, audio_seconds: {_gt: 0}}
        order_by: {users_count: desc}
        limit: 10
    ) {
        id
        title
        asin
        audio_seconds
        publisher {
            name
        }
        cached_contributors
        book {
            title
            rating
        }
    }
}
`} title="Audiobook Editions"/>
````

## File: src/content/docs/api/GraphQL/Schemas/Goals.mdx
````
---
title: Goals
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Images.mdx
````
---
title: Images
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Languages.mdx
````
---
title: Languages
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Likes.mdx
````
---
title: Likes
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Lists.mdx
````
---
title: Lists
category: reference
lastUpdated: 2025-08-03 00:00:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import {Aside} from "@astrojs/starlight/components";

# What Is a List?

Lists in Hardcover are user-created collections of books organized around themes, genres, or personal preferences. Users can create public or private lists to organize and share their reading recommendations with the community.

# Queries

## Available List Queries

<table>
    <thead>
    <tr>
        <th>Query</th>
        <th>Returns</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>lists</td>
        <td>lists[]</td>
        <td>Fetch an array of lists with filtering and pagination</td>
    </tr>
    <tr>
        <td>lists_aggregate</td>
        <td>lists_aggregate</td>
        <td>Get aggregated data about lists (count, averages, etc.)</td>
    </tr>
    <tr>
        <td>lists_by_pk</td>
        <td>lists</td>
        <td>Fetch a single list by its primary key (id)</td>
    </tr>
    <tr>
        <td>list_books</td>
        <td>list_books[]</td>
        <td>Fetch books in lists with filtering options</td>
    </tr>
    <tr>
        <td>list_books_aggregate</td>
        <td>list_books_aggregate</td>
        <td>Get aggregated data about books in lists</td>
    </tr>
    <tr>
        <td>list_books_by_pk</td>
        <td>list_books</td>
        <td>Fetch a single list book entry by its id</td>
    </tr>
    <tr>
        <td>followed_lists</td>
        <td>followed_lists[]</td>
        <td>Fetch lists followed by users</td>
    </tr>
    <tr>
        <td>followed_lists_by_pk</td>
        <td>followed_lists</td>
        <td>Fetch a single followed list entry by id</td>
    </tr>
    </tbody>
</table>

## List Schema Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>int</td>
        <td>Unique identifier for the list</td>
    </tr>
    <tr>
        <td>name</td>
        <td>string</td>
        <td>The title/name of the list</td>
    </tr>
    <tr>
        <td>description</td>
        <td>string</td>
        <td>Description of the list's purpose or theme</td>
    </tr>
    <tr>
        <td>slug</td>
        <td>string</td>
        <td>URL-friendly identifier for the list</td>
    </tr>
    <tr>
        <td>books_count</td>
        <td>int</td>
        <td>Total number of books in the list</td>
    </tr>
    <tr>
        <td>likes_count</td>
        <td>int</td>
        <td>Number of users who have liked this list</td>
    </tr>
    <tr>
        <td>public</td>
        <td>bool</td>
        <td>Whether the list is publicly visible</td>
    </tr>
    <tr>
        <td>privacy_setting_id</td>
        <td>int</td>
        <td>Privacy setting for the list: 1 = public, 2 = followers only, 3 = private</td>
    </tr>
    <tr>
        <td>user_id</td>
        <td>int</td>
        <td>ID of the user who created the list</td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>timestamp</td>
        <td>When the list was created</td>
    </tr>
    <tr>
        <td>updated_at</td>
        <td>timestamp</td>
        <td>When the list was last modified</td>
    </tr>
    <tr>
        <td>user</td>
        <td>User</td>
        <td>User object of the list creator</td>
    </tr>
    <tr>
        <td>list_books</td>
        <td>ListBook[]</td>
        <td>Array of books associated with this list</td>
    </tr>
    </tbody>
</table>

## ListBook Schema Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>int</td>
        <td>Unique identifier for the list_book entry</td>
    </tr>
    <tr>
        <td>list_id</td>
        <td>int</td>
        <td>ID of the list containing this book</td>
    </tr>
    <tr>
        <td>book_id</td>
        <td>int</td>
        <td>ID of the book in this list</td>
    </tr>
    <tr>
        <td>edition_id</td>
        <td>int</td>
        <td>Optional specific edition of the book</td>
    </tr>
    <tr>
        <td>position</td>
        <td>int</td>
        <td>Order position of the book in the list</td>
    </tr>
    <tr>
        <td>date_added</td>
        <td>timestamptz</td>
        <td>When the book was added to the list</td>
    </tr>
    <tr>
        <td>book</td>
        <td>books</td>
        <td>The book object</td>
    </tr>
    <tr>
        <td>list</td>
        <td>lists</td>
        <td>The list object</td>
    </tr>
    <tr>
        <td>edition</td>
        <td>editions</td>
        <td>Optional edition object</td>
    </tr>
    </tbody>
</table>

## Related Schemas

- [Books](/api/graphql/schemas/books) - Books that can be added to lists
- [Users](/api/graphql/schemas/users) - Users who create and interact with lists
- [Editions](/api/graphql/schemas/editions) - Specific editions of books

# Example Queries

## Get All Public Lists

Retrieve the top 10 most-liked public lists.

<GraphQLExplorer query={`
query GetPublicLists {
    lists(
        where: {public: {_eq: true}}
        order_by: {likes_count: desc}
        limit: 10
    ) {
        id
        name
        description
        books_count
        likes_count
        user {
            username
        }
    }
}
`} title="Public Lists"/>

## Get Lists by a Specific User

Get all lists created by a specific user. Replace ##USER_ID## with the actual user ID.

<GraphQLExplorer query={`
query GetUserLists {
    lists(
        where: {user_id: {_eq: ##USER_ID##}}, 
        order_by: {updated_at: desc}
    ) {
        id
        name
        description
        books_count
        public
        created_at
        updated_at
    }
}
`}
    title="User Lists"
    canTry={false}
/>

## Get Books in a Specific List

Get all books in a specific list with their details.

This example uses NPR Top 100 Science Fiction Fantasy list (ID: 3).

<Aside type="note">
    The list must be public or owned by the authenticated user.
</Aside>

<GraphQLExplorer query={`
query GetListBooks {
    lists(where: {id: {_eq: 3}}) {
        name
        description
        list_books {
            book {
                id
                title
                contributions {
                    author {
                        name
                    }
                }
                rating
                pages
            }
            position
            date_added
        }
    }
}
`} title="List Books"/>

## Get a Single List by ID

Fetch a specific list using its primary key.

<GraphQLExplorer query={`
query GetListById {
    lists_by_pk(id: 3) {
        id
        name
        description
        books_count
        likes_count
        privacy_setting_id
        created_at
        updated_at
        user {
            id
            username
            image_id
        }
    }
}
`} title="Get List by ID"/>

## Get List Statistics

Use aggregate queries to get statistics about lists.

<GraphQLExplorer query={`
query GetListStats {
    lists_aggregate(where: {public: {_eq: true}}) {
        aggregate {
            count
            avg {
                books_count
                likes_count
            }
            max {
                books_count
                likes_count
            }
        }
    }
}
`} title="List Statistics"/>

## Get Followed Lists

Get all lists that the authenticated user is following.

<GraphQLExplorer query={`
query GetMyFollowedLists {
    followed_lists(order_by: {created_at: desc}) {
        id
        created_at
        list {
            id
            name
            description
            books_count
            likes_count
            user {
                username
            }
        }
    }
}
`} title="Followed Lists"/>

## Get Lists by Popularity

Find public lists ordered by popularity.

<Aside type="note">
    The Hardcover API doesn't support text search operators like _ilike for lists. Use exact matches or browse public lists by popularity.
</Aside>

<GraphQLExplorer query={`
query GetPopularLists {
    lists(
        where: {public: {_eq: true}}
        limit: 20
        order_by: {likes_count: desc}
    ) {
        id
        name
        description
        books_count
        likes_count
        user {
            username
        }
    }
}
`} title="Popular Lists"/>

# Mutations

## Available List Mutations

<table>
    <thead>
    <tr>
        <th>Mutation</th>
        <th>Returns</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>insert_list</td>
        <td>ListIdType</td>
        <td>Create a new list</td>
    </tr>
    <tr>
        <td>update_list</td>
        <td>ListIdType</td>
        <td>Update an existing list</td>
    </tr>
    <tr>
        <td>delete_list</td>
        <td>ListDeleteType</td>
        <td>Delete a list (must be owner)</td>
    </tr>
    <tr>
        <td>insert_list_book</td>
        <td>ListBookIdType</td>
        <td>Add a book to a list</td>
    </tr>
    <tr>
        <td>delete_list_book</td>
        <td>ListBookDeleteType</td>
        <td>Remove a book from a list</td>
    </tr>
    <tr>
        <td>update_list_books</td>
        <td>list_books_mutation_response</td>
        <td>Update multiple list book entries</td>
    </tr>
    <tr>
        <td>upsert_followed_list</td>
        <td>FollowedListType</td>
        <td>Follow or unfollow a list</td>
    </tr>
    <tr>
        <td>delete_followed_list</td>
        <td>DeleteListType</td>
        <td>Unfollow a list</td>
    </tr>
    </tbody>
</table>

## Mutation Response Types

List mutations return different response types based on the operation:

### ListIdType (for insert_list, update_list)
<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>Int</td>
        <td>ID of the created/updated list</td>
    </tr>
    <tr>
        <td>list</td>
        <td>lists</td>
        <td>The complete list object</td>
    </tr>
    <tr>
        <td>errors</td>
        <td>String</td>
        <td>Any error messages</td>
    </tr>
    </tbody>
</table>

### ListBookIdType (for insert_list_book)
<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>Int</td>
        <td>ID of the created list_book entry</td>
    </tr>
    <tr>
        <td>list_book</td>
        <td>list_books</td>
        <td>The complete list_book object</td>
    </tr>
    </tbody>
</table>

### ListDeleteType (for delete_list) and DeleteListType (for delete_followed_list)
<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>success</td>
        <td>Boolean!</td>
        <td>Whether the deletion was successful</td>
    </tr>
    </tbody>
</table>

## Create a New List

Create a new list with name, description, and privacy setting.

**Privacy settings:**
- `1` = public
- `2` = followers only  
- `3` = private

<Aside type="note">
    New lists may take a few minutes to appear on the website due to caching.
</Aside>

<GraphQLExplorer query={`
mutation CreateList {
    insert_list(
        object: {
            name: "My Favorite Sci-Fi Books"
            description: "A collection of the best science fiction novels I've read"
            privacy_setting_id: 1
        }
    ) {
        affected_rows
        returning {
            id
            name
            description
            public
            created_at
            user {
                username
            }
        }
    }
}
`} title="Create List"/>

## Add a Book to a List

Add a book to your own list.

<Aside type="note">
    You can only add books to lists you own. The position field determines the order of books in the list.
</Aside>

<GraphQLExplorer query={`
mutation AddBookToList {
    insert_list_book(
        object: {
            list_id: 27818
            book_id: 456
            position: 1
        }
    ) {
        id
        list_book {
            id
            list_id
            book_id
            position
            date_added
            book {
                title
            }
            list {
                name
            }
        }
    }
}
`} title="Add Book to List"/>

## Update a List

Update an existing list's details.

<Aside type="note">
    You can only update lists you own. The object parameter accepts the same fields as when creating a list.
</Aside>

<GraphQLExplorer query={`
mutation UpdateList {
    update_list(
        id: 27818
        object: {
            name: "Updated List Name"
            description: "This is the updated description for my list"
            privacy_setting_id: 2
        }
    ) {
        id
        list {
            id
            name
            description
            privacy_setting_id
            updated_at
        }
    }
}
`} title="Update List"/>

## Delete a List

Delete a list you own.

<Aside type="caution">
    This action is irreversible. All books in the list will be removed as well.
</Aside>

<GraphQLExplorer query={`
mutation DeleteList {
    delete_list(id: 27818) {
        success
    }
}
`} title="Delete List"/>

## Remove a Book from a List

Remove a specific book from your list.

<GraphQLExplorer query={`
mutation RemoveBookFromList {
    delete_list_book(id: 123456) {
        id
        list_id
        list {
            name
            books_count
        }
    }
}
`} title="Remove Book from List"/>

## Follow/Unfollow a List

Follow a public list to track updates. This mutation acts as an upsert - it will create a follow if it doesn't exist.

<GraphQLExplorer query={`
mutation FollowList {
    upsert_followed_list(list_id: 3) {
        id
        followed_list {
            id
            list_id
            user_id
            created_at
            list {
                name
                user {
                    username
                }
            }
        }
    }
}
`} title="Follow List"/>

## Unfollow a List

Remove a list from your followed lists.

<GraphQLExplorer query={`
mutation UnfollowList {
    delete_followed_list(list_id: 3) {
        success
    }
}
`} title="Unfollow List"/>
````

## File: src/content/docs/api/GraphQL/Schemas/Notifications.mdx
````
---
title: Notifications
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Platforms.mdx
````
---
title: Platforms
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Prompts.mdx
````
---
title: Prompts
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Publishers.mdx
````
---
title: Publishers
category: reference
lastUpdated: 2025-06-07 18:30:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import {Aside} from "@astrojs/starlight/components";

# What Is a Publisher?

A Publisher in Hardcover represents a company or organization that publishes books. Publishers are linked to specific editions of books, as the same book may be published by different publishers in different regions or formats. Publishers help users find books from their favorite publishing houses and understand the publishing history of editions.

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>bigint</td>
        <td>Unique identifier for the publisher</td>
    </tr>
    <tr>
        <td>name</td>
        <td>string</td>
        <td>The name of the publisher</td>
    </tr>
    <tr>
        <td>slug</td>
        <td>string</td>
        <td>URL-friendly identifier for the publisher</td>
    </tr>
    <tr>
        <td>canonical_id</td>
        <td>int</td>
        <td>Canonical ID for merged publishers</td>
    </tr>
    <tr>
        <td>parent_id</td>
        <td>int</td>
        <td>ID of the parent publisher (for imprints)</td>
    </tr>
    <tr>
        <td>editions_count</td>
        <td>int</td>
        <td>Number of editions published by this publisher</td>
    </tr>
    <tr>
        <td>locked</td>
        <td>bool</td>
        <td>Whether the publisher is locked from editing</td>
    </tr>
    <tr>
        <td>state</td>
        <td>string</td>
        <td>Current state of the publisher record</td>
    </tr>
    <tr>
        <td>user_id</td>
        <td>int</td>
        <td>ID of the user who created the publisher</td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>timestamp</td>
        <td>When the publisher was created</td>
    </tr>
    <tr>
        <td>updated_at</td>
        <td>timestamp</td>
        <td>When the publisher was last updated</td>
    </tr>
    <tr>
        <td>editions</td>
        <td>Edition[]</td>
        <td>Array of editions published by this publisher</td>
    </tr>
    <tr>
        <td>parent_publisher</td>
        <td>Publisher</td>
        <td>Parent publisher object (for imprints)</td>
    </tr>
    </tbody>
</table>

# Related Schemas

- [Editions](/api/graphql/schemas/editions) - Editions published by publishers
- [Books](/api/graphql/schemas/books) - Books have multiple editions from different publishers
- [Authors](/api/graphql/schemas/authors) - Authors work with various publishers

# Example Queries

## Get Publisher Details

Retrieve detailed information about a specific publisher including recent editions. This example uses Penguin Random House (ID: 1).

<GraphQLExplorer query={`
query GetPublisherDetails {
    publishers(where: {id: {_eq: 1}}) {
        id
        name
        slug
        editions_count
        parent_publisher {
            name
        }
        editions(
            limit: 5
            order_by: {release_date: desc}
        ) {
            id
            title
            isbn_13
            release_date
            book {
                title
                contributions {
                    author {
                        name
                    }
                }
            }
        }
    }
}
`} title="Publisher Details"/>

## Find Publishers by Name

Search for publishers by name pattern. This example searches for publishers with "Penguin" in the name.

<GraphQLExplorer query={`
query FindPublishers {
    publishers(
        where: {name: {_eq: "Penguin Random House"}}
        order_by: {editions_count: desc}
        limit: 10
    ) {
        id
        name
        editions_count
        parent_publisher {
            name
        }
    }
}
`} title="Publisher Search"/>

## Get Books by Publisher

Find all books published by a specific publisher, showing different editions.

<Aside type="note">
    This query shows unique books (not editions) published by the publisher, grouped by the parent book.
</Aside>

<GraphQLExplorer query={`
query GetPublisherBooks {
    publishers(where: {id: {_eq: 1}}) {
        name
        editions(
            order_by: {book: {title: asc}}
            limit: 5
        ) {
            id
            isbn_13
            physical_format
            pages
            release_date
            book {
                id
                title
                rating
                contributions {
                    author {
                        name
                    }
                }
            }
        }
    }
}
`} title="Publisher Books"/>


## Get Popular Publishers

Retrieve the most active publishers by edition count.

<GraphQLExplorer query={`
query GetPopularPublishers {
    publishers(
        where: {editions_count: {_gt: 100}}
        order_by: {editions_count: desc}
        limit: 5
    ) {
        id
        name
        slug
        editions_count
        editions(
            limit: 3
            order_by: {book: {rating: desc}}
        ) {
            book {
                title
                rating
            }
        }
    }
}
`} title="Popular Publishers"/>
````

## File: src/content/docs/api/GraphQL/Schemas/ReadingFormats.mdx
````
---
title: Reading Formats
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/ReadingJournals.mdx
````
---
title: Reading Journals
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Recommendations.mdx
````
---
title: Recommendations
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Series.mdx
````
---
title: Series
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Tags.mdx
````
---
title: Tags
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/api/GraphQL/Schemas/Users.mdx
````
---
title: Users
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## What Is a User?

Users are the people who use the Hardcover platform.
Users can perform actions like adding books to their shelves, following other users, and writing reviews.

## User Schema

The user schema contains the following fields:

### Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>Int</td>
        <td>The unique identifier of the user</td>
    </tr>
    <tr>
        <td>username</td>
        <td>String</td>
        <td>The username of the user</td>
    </tr>
    <tr>
        <td>birthdate</td>
        <td>String</td>
        <td>The birthdate of the user</td>
    </tr>
    <tr>
        <td>books_count</td>
        <td>Int</td>
        <td>The number of books the user has added</td>
    </tr>
    <tr>
        <td>flair</td>
        <td>String</td>
        <td>The flair of the user</td>
    </tr>
    <tr>
        <td>followers_count</td>
        <td>Int</td>
        <td>The number of followers the user has</td>
    </tr>
    <tr>
        <td>followed_users_count</td>
        <td>Int</td>
        <td>The number of users the user follows</td>
    </tr>
    <tr>
        <td>location</td>
        <td>String</td>
        <td>The location of the user</td>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>The name of the user</td>
    </tr>
    <tr>
        <td>pro</td>
        <td>Boolean</td>
        <td></td>
    </tr>
    <tr>
        <td>pronoun_personal</td>
        <td>String</td>
        <td>The personal pronoun of the user</td>
    </tr>
    <tr>
        <td>pronoun_possessive</td>
        <td>String</td>
        <td>The possessive pronoun of the user</td>
    </tr>
    <tr>
        <td>sign_in_count</td>
        <td>Int</td>
        <td>The number of times the user has signed in</td>
    </tr>
    </tbody>
</table>

## Related Schemas

- me &mdash; The currently authenticated user

## Example Queries

### Get My User Information
<GraphQLExplorer query={`
query {
      me {
            id
            username
            birthdate
            books_count
            flair
            followers_count
            followed_users_count
            location
            name
            pro
            pronoun_personal
            pronoun_possessive
            sign_in_count
      }
}`} description={`Get information for the current user`}
    title="My Information"
/>

### Get a User by ID

<GraphQLExplorer query={`
query {
    users(where: {id: {_eq: 1}}, limit: 1) {
        id,
        username
  }
}
`} title="User by ID"/>

### Get a User by Username

<GraphQLExplorer query={`
query {
    users(where: {username: {_eq: "adam"}}, limit: 1) {
        id,
        username
    }
}
`} title="User by Username"/>
````

## File: src/content/docs/api/guides/GettingAllBooksInLibrary.mdx
````
---
title: Getting Books in Your Library
category: guide
lastUpdated: 2025-08-13
layout: /src/layouts/documentation.astro
---
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

This guide will show you how to get a list of the books in your library using the Hardcover API. Books are considered "in your library" when they have been marked "Want to Read", "Currently Reading", etc.

## Related Schemas

- [Books](../../api/graphql/schemas/books)

## Get a List of Books in a User’s Library

To see a selection of the books in your library, replace `##USER_ID##` with your account id, which can be found by completing the "Example Request" section of the [Getting Started](../../api/getting-started) guide.

<GraphQLExplorer query={`
{
      user_books(
            where: {
                user_id: {_eq: ##USER_ID##}
            },
            distinct_on: book_id
            limit: 5
            offset: 0
      ) {
        book {
              title
              pages
              release_date
        }
      }
}
`} description={`
    This query will return a list of books that the user has added to their collection.
`} title="User Books" presentation='json'/>
````

## File: src/content/docs/api/guides/GettingBookDetails.mdx
````
---
title: Getting Book Details
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Related Schemas
- [Books](/api/graphql/schemas/books)
- [Editions](/api/graphql/schemas/editions)

## Getting All Editions of a Book
<GraphQLExplorer query={`
query GetEditionsFromTitle {
    editions(where: {title: {_eq: "Oathbringer"}}) {
        id
        title
        edition_format
        pages
        release_date
        isbn_10
        isbn_13
        publisher {
            name
        }
    }
}
`} description='Get all of the editions for the specific title of `Oathbringer`' title="Editions From Title" presentation='json' forcePresentation />

## Getting Details of a Specific Edition
<GraphQLExplorer query={
`query GetSpecificEdition {
    editions(where: {id: {_eq: 21953653}}) {
        book {
            title
            release_date
            slug
            subtitle
            contributions {
                author {
                    name
                }
            }
        }
    }
}`} description='Get the details of the specific edition of Oathbringer as a physical book published by Tor'/>
````

## File: src/content/docs/api/guides/GettingBooksProgress.mdx
````
---
title: Getting Progress of Books
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

### Example Request
<GraphQLExplorer query={``} description='' />
````

## File: src/content/docs/api/guides/GettingBooksWithStatus.mdx
````
---
title: Getting Books With a Status
category: guide
lastUpdated: 2025-08-31 
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

This guide will show you how to get a user's books with a specific status.

## Related Schemas
- [Books](/api/graphql/schemas/books)

### Get a List of Books With a Status

To see a selection of the books in your library, replace `##USER_ID##` with your account id, which can be found by completing the "Example Request" section of the [Getting Started](../../api/getting-started) guide. To change the [book status](/api/graphql/schemas/books#user-book-statuses) being queried for, replace the `2` (which represents the "Currently Reading" status) with your desired status.

<GraphQLExplorer query={`
{
    user_books(
        where: {user_id: {_eq: ##USER_ID##}, status_id: {_eq: 2}}
    ) {
        book {
            title
            image {
                url
            }
            contributions {
                author {
                    name
                }
            }
        }
    }
}
`} description={`
    This query will return a list of books that the user has in the "Currently Reading" status.
`} title="Books By Status" presentation='json' />
````

## File: src/content/docs/api/guides/Searching.mdx
````
---
title: Searching for Content in the API
description: Search for books, authors, and other content using the Hardcover GraphQL API.
category: guide
lastUpdated: 2025-05-02 23:50:00
layout: /src/layouts/documentation.astro
---

import {Aside} from "@astrojs/starlight/components";
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## What Can I Search For?

Currently, you can search for authors, books, characters, lists, prompts, publishers, series, and users.
Additional search options will be added in the future.

Behind the scenes, Hardcover uses [Typesense](https://typesense.org/) for search. This same Typesense
index used on the website is used for this endpoint.

The search API does not currently support filtering by parameters besides `query`, however you can
change which attributes (columns) are searched as well as changing sorting.

## Search Options

Only `query` is required. If all other fields are blank, this will default to the same search as the Hardcover website when searching for a book.

- `query`* - The search term
- `query_type` - The type of content to search for one of (case-insensitive; default `book`)
                    - `author`
                    - `book`
                    - `character`
                    - `list`
                    - `prompt`
                    - `publisher`
                    - `series`
                    - `user`
- `per_page` - The number of results to return per page (default 25)
- `page` - The page number to return (default 1)
- `sort` - What attributes should the result be sorted by
- `fields` - Which attributes within the given `query_type` to include in the search
- `weights` - A comma separated list of numbers indicating weights to give each of the `fields` when calculating match

<Aside type="note">
    `fields` and `weights` are used togther. If you pass in 2 fields to
    search (ex: `name,name_personal`), you'll also need to pass in 2 weights (`5,1`).
    Weights are relative to each other.
</Aside>

<Aside type="note" title="Note #2">
    Some fields for an object contain other objects or numerical data
    isn't useful for filtering, but could come in handy for sorting or to show
    more information about an entity.
</Aside>


## Available Fields

- `ids` - Array of `id` attributes for results in order
- `results` - Result objects returned from Typesense
- `query` - Passed in `query`, or default
- `query_type` - Passed in `query_type`, or default
- `page` - Passed in `page`, or default
- `per_page` - Passed in `per_page`, or default

## Example Searches

### Authors

The following fields are available in the returned object. You can also `sort` by any of these, or limit you search to specific field(s) using `fields` and `weights`.

- `alternate_names` - Alternative names for the author
- `books` - Titles of the top 5 most popular books by this author
- `books_count` - Number of books by this author
- `image` - Image object containing image URL, dimensions, color, etc.
- `name` - The name of the author
- `name_personal` - The personal name of the author
- `series_names` - The names of the different series the author has written
- `slug` - The URL slug of this author

#### Default Values

When searching authors, we use the following default values.

- `fields`: `name,name_personal,alternate_names,series_names,books`
- `sort`: `_text_match:desc,books_count:desc`
- `weights`: `3,3,3,2,1`

<GraphQLExplorer query={`
    query BooksByRowling {
        search(
            query: "rowling",
            query_type: "Author",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of books written by Rowling.
`} title="Search Authors" presentation='json' forcePresentation/>

### Books

The following fields are available in the returned object. You can also `sort` by any of these, or limit you search to specific field(s) using `fields` and `weights`.

- `activities_count` - Number of activities for this book
- `alternative_titles` - Alternative titles for the book
- `audio_seconds` - Number of seconds for the default audiobook edition
- `author_names` - The name of the authors or contributors of the book
- `compilation` - Boolean if this book is a compilation
- `content_warnings` - Top 5 content warnings
- `contribution_types` - Array of contribution types for contributions
- `contributions` - Array of contribution objects
- `cover_color` - The extracted color of the book (ex: `red`, `green`)
- `description` - The description of the book
- `featured_series` - Object containing information about the series
- `featured_series_position` - Number indicating the featured series position
- `genres` - Top 5 genres
- `isbns` - The ISBNs of the book
- `lists_count` - Number of lists this book is on
- `has_audiobook` - Boolean if known to have an audiobook 
- `has_ebook` - Boolean if known to have an ebook 
- `moods` - Top 5 moods
- `pages` - Number of pages of the default physical edition
- `prompts_count` - Number of prompts this book is on
- `rating` - Hardcover average rating
- `ratings_count` - Number of Hardcover ratings
- `release_date_i` - The release date as an integer
- `release_year` - Date the book was published
- `reviews_count` - Number of Hardcover reviews
- `series_names` - The name of the series the book belongs to
- `slug` - The URL slug of the book
- `subtitle` - The subtitle of the book
- `tags` - Top 5 tags
- `title` - The title of the book
- `users_count` - Number of Hardcover users who have saved this book
- `users_read_count` - Count of users who have marked this book as read

#### Default Values

When searching books, we use the following default values.

- `fields`: `title,isbns,series_names,author_names,alternative_titles`
- `sort`: `_text_match:desc,users_count:desc`
- `weights`: `5,5,3,1,1`

<GraphQLExplorer query={`
    query LordOfTheRingsBooks {
        search(
            query: "lord of the rings",
            query_type: "Book",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of books belonging to the Lord of the Rings series.
`} title="Search Books" presentation='json' forcePresentation />

### Characters

The following fields are available in the returned object. You can also `sort` by any of these, or limit you search to specific field(s) using `fields` and `weights`.

- `author_names` - The name of the author who wrote the books the character appears in
- `books` - A list of book titles with release year the character appears in (only includes books for which this character being present is not considered a spoiler)
- `books_count` - Total number of books this character has been in
- `name` - The name of the character
- `object_type` - The string "Character"
- `slug` - The URL slug for this character

#### Default Values

When searching characters, we use the following default values.

- `fields`: `name,books,author_names`
- `sort`: `_text_match:desc,books_count:desc`
- `weights`: `4,2,2`

<GraphQLExplorer query={`
    query CharactersNamedPeter {
        search(
            query: "peter",
            query_type: "Character",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of characters named Peter.
`} title="Search Characters" presentation='json' forcePresentation />

### Lists

The following fields are available in the returned object. You can also `sort` by any of these, or limit you search to specific field(s) using `fields` and `weights`.

- `description` - The description of the list
- `books` - Titles of the first 5 books
- `books_count` - Number of books in this list
- `likes_count` - Number of likes for this list
- `object_type` - The string "List"
- `name` - The name of the list
- `slug` - The URL slug of the list
- `user` - User object of the list owner

#### Default Values

When searching lists, we use the following default values.

- `fields`: `name,description,books`
- `sort`: `_text_match:desc,likes_count:desc`
- `weights`: `3,2,1`

<GraphQLExplorer query={`
    query ListsNamedBest {
        search(
            query: "best",
            query_type: "List",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of lists with the word "best" in the name.
`} title="Search Lists" presentation='json' forcePresentation />

### Prompts

The following fields are available in the returned object. You can also `sort` by any of these, or limit you search to specific field(s) using `fields` and `weights`.

- `answers_count` - Number of total upvote answers
- `books` - Titles of the top 5 most upvoted books for this prompt
- `books_count` - Number of unique books upvoted
- `question` - The prompt question
- `slug` - The URL slug
- `user` - User object of the prompt creator
- `users_count` - Number of users who have answered this prompt

#### Default Values

When searching prompts, we use the following default values.

- `fields`: `question,books`
- `sort`: `_text_match:desc`
- `weights`: `2,1`

<GraphQLExplorer query={`
    query PromptsAboutLearning {
        search(
            query: "learn from",
            query_type: "Prompt",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of prompts about learning from books.
`} title="Search Prompts" presentation='json' forcePresentation />

### Publishers

The following fields are available in the returned object. You can also `sort` by any of these, or limit you search to specific field(s) using `fields` and `weights`.

- `editions_count` - Number of editions with this publisher
- `name` - The name of the publisher
- `object_type` - The string "Publisher"
- `slug` - The URL slug of the publisher

#### Default Values

When searching publishers, we use the following default values.

- `fields`: `name`
- `sort`: `_text_match:desc,editions_count:desc`
- `weights`: `1`

<GraphQLExplorer query={`
    query PublishersNamedPenguin {
        search(
            query: "penguin",
            query_type: "Publisher",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of publishers with the word "penguin" in the name.
`} title="Search Publishers" presentation='json' forcePresentation />

### Series

The following fields are available in the returned object. You can also `sort` by any of these, or limit you search to specific field(s) using `fields` and `weights`.

- `author_name` - The name of the primary author who wrote the series
- `author` - Author object
- `books_count` - Number of books in this series
- `books` - A list of books in the series
- `name` - The name of the series
- `primary_books_count` - Number of books in this series with an Integer position (1, 2, 3; exlcludes 1.5, empty)
- `readers_count` - Sum of `books.users_read_count` for all books in this series (_not distinct, so readers will be counted once per book_)
- `slug` - The URL slug of the series

#### Default Values

When searching series, we use the following default values.

- `fields`: `name,books,author_name`
- `sort`: `_text_match:desc,readers_count:desc`
- `weights`: `2,1,1`

<GraphQLExplorer query={`
    query SeriesNamedHarryPotter {
        search(
            query: "harry potter",
            query_type: "Series",
            per_page: 7,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of series with the words "harry potter" in the name.
`} title="Search Series" presentation='json' forcePresentation />

### Users

The following fields are available in the returned object. You can also `sort` by any of these, or limit you search to specific field(s) using `fields` and `weights`.

- `books_count` - Number of books in this users library (any status)
- `flair` - Custom flair for this user
- `followed_users_count` - Number of users this user follows
- `followers_count` - Number of followers for this user
- `image` - Image object
- `location` - The location of the user
- `name` - The name of the user
- `pro` - Boolean if a supporter
- `username` - The username of the user

#### Default Values

When searching users, we use the following default values.

- `sort`: `_text_match:desc,followers_count:desc`
- `fields`: `name,username,location`
- `weights`: `2,2,1`

<GraphQLExplorer query={`
    query UsersNamedAdam {
        search(
            query: "adam",
            query_type: "User",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of users with the name "adam".
`} title="Search Users" presentation='json' forcePresentation />
````

## File: src/content/docs/api/guides/UpdatingABooksProgress.mdx
````
---
title: Updating a Book's Progress and Dates Read
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

This guide will show you how to update a book's progress and dates read.

### Example Request
<GraphQLExplorer query={``} description='' />
````

## File: src/content/docs/api/guides/UpdatingReadingJournal.mdx
````
---
title: Updating Reading Journal
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
draft: true
---
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

This guide will walk you through how to update a book's reading journal.
This includes updating the progress of the book, the dates read, and the notes you've taken.

### Example Request
<GraphQLExplorer query={``} description='' />
````

## File: src/content/docs/api/Getting-Started.mdx
````
---
title: Getting Started with the API
description: Get started with the Hardcover GraphQL API.
category: guide
lastUpdated: 2025-07-21 17:22:00
layout: /src/layouts/documentation.astro
---

import {Badge, Steps} from "@astrojs/starlight/components";
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import { URLS } from "@/Consts";

## Introduction
Our API is accessible using GraphQL. The API that you can use is exactly the same API used by the website, iOS and Android apps.
This means that you can build your own tools and services that interact with the same data that you see on the website.

The API is currently in beta, and we are actively working on it.
We are currently looking for feedback on this API.

### Getting Started Quick Guide
<Steps>
    1. Get your API key
    2. Make your first request
    3. Read the API references and Guides on this site
    4. Build something awesome and share it with us on <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>!
</Steps>

## Getting Help
If you have any questions or need help, please reach out to us on <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>.

## Getting an API Key
To get an API token, you need to go to your account settings page and click on the <a href={URLS.API_ACCOUNT_URL} target="_blank" rel="noreferrer noopener">Hardcover API</a> link; the token will be available at the top of the page.
the token will be available at the top of the page.

API tokens are not meant to be shared and should be kept private, as they can be used to access your account and data.

After you have your token, you can start making requests to the API.

## Making Your First Request
After you have your token, you can head over to the [GraphQL console](https://cloud.hasura.io/public/graphiql?endpoint=https://api.hardcover.app/v1/graphql).

Next, add a **header** called `authorization` with your token as the value.

<img src="/images/api/getting-started/graphql-authorization-header.png" alt="Example of the authorization header" />

Tab or click out of the field, and you should see a list of available resources.

### Example Request
To test that it's working, go to the `Try it Yourself` tab below
- Add your token to the `Authorization Token` field.
<img src="/images/api/getting-started/graphql-explorer-token-field.png" alt="Showing the location of the Authorization Token field in the GraphQL Explorer" />
- Then click the `Run Query` button.

You should see your user ID and username in the Results section.

<GraphQLExplorer query={`
query {
    me {
        id,
        username
    }
}
`} title="Example Request"/>

## API Response Codes
The API will return the following response codes:

| Code | Description                                                  | Example Body                                |
|------|--------------------------------------------------------------|---------------------------------------------|
| 200  | The request was successful                                   |                                             |
| 401  | Expired or invalid token                                     | `{ error: "Unable to verify token" }`       |
| 403  | User does not have access to the requested resource or query | `{ error: "Message describing the error" }` |
| 404  | Not Found                                                    |                                             |
| 429  | Too Many Requests, try again later                           | `{ error: "Throttled" }`                    |
| 500  | Internal Server Error                                        | `{ error: "An unknown error occurred" }`    |

## Important Notes About the Hardcover API
- The API is still heavily in flux right now. Anything you build using it could break in the future.
- We may reset tokens without notice while in beta.
- The same ownership rights exist for this as anything on the site.
    - You own your data.
    - This means you can't use the API to access and use someone else's data.
- This API is running the same as if you were using the browser. Any actions you take will be under your user.
- <Badge text="Don't share your token! Someone could delete your account with it." variant="danger" />
- This should only be used from a code backend — never from a browser.
- This is only for offline use at this time.
    - You can only access this API from localhost or APIs.
    - Later on, we hope to allow developers to join a group that allowlists specific sites, but that's a way down the line.
- <Badge text="Recommendation" variant="note" /> When authoring scripts that use the API, it is recommended to include a user-agent header with a description of the script.
- API calls are rate-limited to 60 requests per minute.
- Queries have a max timeout of 30 seconds.

## Limitations
- API tokens automatically expire after 1 year, and reset on January 1st.
- API is rate-limited to 60 requests per minute.
- The following queries are disabled:
    - `_like`
    - `_nlike`
    - `_ilike`
    - `_niregex`
    - `_nregex`
    - `_iregex`
    - `_regex`
    - `_nsimilar`
    - `_similar`
- Queries have a max timeout of 30 seconds.
- Queries are not allowed to run in the browser, they must be run in an environment where the token can be kept secure.
- <Badge text="2025" variant="note" /> Queries have a maximum depth of 3.
- <Badge text="2025" variant="note" /> Queries are limited to your own user data, public data, and user data of users you follow.
- <Badge text="2025" variant="note" /> OAuth support will be added for external applications.

## Want to Contribute?
We are actively looking for contributors to help us improve the API documentation.

For more information about how to contribute to the API Documentation, please see the [Contributing Guide](/contributing/api-docs).

## Further Reading
- [GraphQL API Reference](https://graphql.org/learn/)
````

## File: src/content/docs/contributing/API-Docs.mdx
````
---
title: API Documentation Guide
category: guide
lastUpdated: 2025-05-02 23:50:00
layout: /src/layouts/documentation.astro
---

import { URLS } from '@/Consts';
import { FileTree } from '@astrojs/starlight/components';

## Developer FAQs

### How Is the Project Structured?

#### File Structure

Starlight looks for `.md` or `.mdx` files in the `src/content/docs/` directory.
Each file is exposed as a route based on its file name.

Images can be added to `src/assets/` and embedded in Markdown with a relative link.

Static assets, like favicons, can be placed in the `public/` directory.

<FileTree>
    - public favicons and other static assets
        - ...
    - src
        - assets Images for doc pages
            - ...
        - components Custom components
            - GraphQLExplorer
                - GraphQLExplorer.astro Main file of the GraphQL Explorer component
                - ...
            - ui shadcn/ui components
                - ...
            - ...
        - content
            - docs mdx files that generates doc pages
                - api
                    - GraphQL
                        - Schema Data schemas
                            - ...
                    - ...
                    - guides Guides and tutorials
                        - ...
                    - getting-started.mdx
                    - ...
                - contributing Contributing guidelines
                    - ...
                - it Italian translations
                    - ...
                -  librarians Librarian guides
                    - ...
                - ui.json translations for any UI strings
        - layouts Layouts for doc pages
            - documentation.astro Main layout for doc pages
            - ...
    - astro.config.mjs Astro configuration file
    - components.json shadcn/ui components
    - CONTRIBUTING Contributing guidelines
    - DEVELOPERS.md Developer FAQs
    - tailwind.config.mjs Tailwind CSS configuration
    - ...
</FileTree>


### How Do I Run the Project Locally?

#### 🚀 Quick Start

1. **Clone the repo:**
```bash
git clone https://github.com/hardcoverapp/hardcover-docs.git
```
2. **Navigate to the project directory:**
```bash
cd hardcover-docs
```
3. **Install dependencies:**
 ```bash
 npm install
  ```
4. **Start the dev server:**
 ```bash
 npm run dev
  ```
5. **Open your browser**
6. **Navigate to `http://localhost:4321`**

#### 🧞 Commands

The Hardcover documentation site is built with [Astro](https://astro.build/).
All commands are run from the root of the project, from a terminal:

| Command                              | Action                                           |
|:-------------------------------------|:-------------------------------------------------|
| `npm install`                        | Installs dependencies                            |
| `npm run dev`                        | Starts local dev server at `localhost:4321`      |
| `npm run build`                      | Build your production site to `./dist/`          |
| `npm run preview`                    | Preview your build locally, before deploying     |
| `npm run astro ...`                  | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help`            | Get help using the Astro CLI                     |
| `npx vitest`                         | Run the unit tests for the project               |
| `npx vitest --coverage.enabled true` | Run the unit tests with code coverage            |

### How Do I Add a New Page or Update an Existing Page?

#### Adding a New Page

1. Create a new `.mdx` file in the `src/content/docs/` directory.
2. Give the file a name that describes the content.
3. Add [frontmatter](../frontmatter) to the top of the file.
4. Add content to the file using Markdown or MDX syntax.
5. Add the new page to the sidebar
 - If the page is part of the `api/GraphQL/Schema` or `guides` sections the sidebar will automatically update with the new page.
 - All other pages will need to be added to the astro config file
see [Starlight - Add links and link groups](https://starlight.astro.build/guides/sidebar/#add-links-and-link-groups)
for more information.

##### Page Frontmatter
Moved to [Frontmatter](../frontmatter)

#### Available Components
Moved to [Astro Components](../astro-components) for Astro components and [React Components](../react-components) for React components.

### Translating Content
Moved to [Translating Documentation Guide](../translating-documentation)

## Support Resources

### Submitting a Bug Report

### Requesting a Feature

### Finding Help on Discord
Connect with us on <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>
````

## File: src/content/docs/contributing/Astro-Components.mdx
````
---
title: Astro Components
category: guide
description: Information about the Astro components available in the documentation site.
lastUpdated: 2025-03-29 17:10:00
layout: /src/layouts/librarians.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import SocialIcons from '@/components/SocialIcons.astro';

## Different Types of Components
Currently, there are two types of components available in the documentation site:
- [**Astro Components**](./astro-components): These are components written in Astro and are used to create static HTML pages. Use these components when you don't need any client-side interactivity. Astro components can be used from other Astro components but can not be used from React components.
- [**React Components**](./react-components): These are components written in React and are used to create dynamic, interactive pages. Use these components when you need client-side interactivity or state management. React components can be used from other React components and from Astro components.

## Writing Astro Components
Astro components are written in `.astro` files in the `/src/components` directory.

## Available Astro Components
In addition to the standard [Starlight - Components](https://starlight.astro.build/guides/components/), the Hardcover
documentation site includes the following custom components:

### GraphQL Explorer

This component allows a user to view GraphQL queries and experiment by running them against the API.

**Import Path:**

```js
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
```

**Parameters:**

- `canTry` - A boolean value determining whether the user can run the query in the explorer. The default is `true`.
- `description` - A string describing the query.
- `forcePresentation` - A boolean value determining whether the presentation options should be hidden. The default is `false`.
- `presentation` - The default presentation of the response, either `json` or `table`. The default is `json`.
- `query` - A string containing the GraphQL query to be displayed in the explorer.
- `title` - A string for the title of the query shown in the explorer. The default is `Example Query`. Change this when translating the page to another language.

**Usage:**

```mdx
<GraphQLExplorer
    query={query}
    description="An example query"
    presentation='table'
    title="Example"
/>
```

<GraphQLExplorer query={`
query {
    me {
        id,
        username
    }
}
`}/>

### Social Icons

This component is mostly meant for internal use, but it can be used to display the hardcover social media icons.

**Import Path:**

```js

import SocialIcons from '@/components/SocialIcons.astro';

```

**Parameters:**

- `iconSize` - A string for the size of the icons. The default is `16px`.

**Usage:**

```mdx
<div class="flex justify-around h-6 w-80">
    <SocialIcons iconSize="20px" />
</div>
```

<div className="flex justify-around h-6 w-80">
    <SocialIcons iconSize="20px" />
</div>

## Limitations
- Astro components are rendered on the server and do not have access to the browser's `window` or `document` objects.
- Astro components do not support client-side state management or interactivity.
- Astro components cannot be used inside React components.
````

## File: src/content/docs/contributing/Frontmatter.mdx
````
---
title: Frontmatter
category: guide
description: Information about the frontmatter used on the documentation pages.
lastUpdated: 2025-03-29 17:10:00
layout: /src/layouts/librarians.astro
---

## What Is Frontmatter?
Frontmatter is a block of metadata at the top of a Markdown file that provides information about the page.
It is used by Starlight to generate the HTML pages and can be used to control various aspects of the page's behavior and appearance.

## What options are available?
The following options are available in the frontmatter for pages:

See [Starlight -
Frontmatter](https://starlight.astro.build/reference/frontmatter/) for more information and additional options.

| Field           | Description                                                                                                                                                                             | Required    |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| title           | String containing the title of the page                                                                                                                                                 | Yes         |
| category        | String of the category the page should be included in `guide` or `reference`                                                                                                            | Yes         |
| layout          | relative path to one of the layouts in `/src/layouts`                                                                                                                                   | Yes         |
| description     | String containing the descriptive text to use in HTML meta tags                                                                                                                         | Recommended |
| lastUpdated     | String in the format `YYYY-MM-DD HH:MM:SS`                                                                                                                                              | Recommended |
| draft           | Boolean value determining whether the page should be hidden from the production site                                                                                                    | No          |
| slug            | String containing the URL slug for the page                                                                                                                                             | No          |
| tableOfContents | Boolean value determining whether a table of contents should be generated                                                                                                               | No          |
| template        | `doc` or `splash` default is `doc`. `splash` is a wider layout without the normal sidebars                                                                                              | No          |
| hero            | See [Starlight - Frontmatter HeroConfig](https://starlight.astro.build/reference/frontmatter/#heroconfig) for more information                                                          | No          |
| banner          | See [Starlight - Frontmatter Banner](https://starlight.astro.build/reference/frontmatter/#banner) for more information                                                                  | No          |
| prev            | Boolean value determining whether a previous button should be shown. See [Starlight - Frontmatter Prev](https://starlight.astro.build/reference/frontmatter/#prev) for more information | No          |
| next            | Boolean value determining whether a next button should be shown. See [Starlight - Frontmatter Next](https://starlight.astro.build/reference/frontmatter/#next) for more information     | No          |
| sidebar         | Control how the page is displayed in the sidebar. See [Starlight - Frontmatter Sidebar](https://starlight.astro.build/reference/frontmatter/#sidebarconfig) for more information        | No          |


### Example Frontmatter

```md
---
title: Getting Started with the API
description: Get started with the Hardcover GraphQL API.
category: guide
lastUpdated: 2025-02-01 17:03:00
layout: ../../layouts/documentation.astro
---
```
````

## File: src/content/docs/contributing/index.mdx
````
---
title: Contributing to Hardcover
description: Get started contributing to Hardcover
lastUpdated: 2025-05-02 23:50:00
sidebar:
    hidden: true
---

import {LinkCard} from "@astrojs/starlight/components";

Welcome to the Hardcover contributing guide!
This is where you can find all the information you need to get started contributing to the Hardcover project.
Whether you're a developer, book enthusiast, or just someone who wants to help out, we welcome your contributions!

## Contributing Guides
<LinkCard title="API Contribution Guide" href="/contributing/api-docs" rel="noreferrer noopener"
          description="Guides more focused on developers, including how to use the API, set up a local environment, and how to contribute to the documentation." />

<LinkCard title="Librarian Contribution Guide" href="/contributing/librarian-guides" rel="noreferrer noopener"
          description="Guides for librarians on how to make edits to books, editions, characters, series, etc." />

<LinkCard title="Translation Guide" href="/contributing/translating-documentation" rel="noreferrer noopener"
          description="We are working on making Hardcover available in multiple languages. If you would like to contribute translations for the documentation this is the place to start." />
````

## File: src/content/docs/contributing/Librarian-Guides.mdx
````
---
title: Librarian Contribution Guide
category: guide
lastUpdated: 2025-03-31 19:28:00
layout: /src/layouts/librarians.astro
---

import { URLS } from "@/Consts";

# Librarian Contribution Guide
## Ways to Contribute
We are currently looking for contributions in the following areas:

- API Documentation: Help us improve the API documentation by adding new pages or updating existing content.
- API Guides: Share your knowledge by writing guides on how to use the Hardcover API.
- Bug Fixes: Help us fix bugs in the documentation site.
- Reporting Issues: Report any issues you encounter with the documentation site. <a href={URLS.CREATE_ISSUE} target="_blank" rel="noreferrer noopener">Create Issue</a>
- Feature Requests: Share your ideas for new features or improvements to the documentation site. <a href={URLS.SUGGEST_FEATURE} target="_blank" rel="noreferrer noopener">Suggest Feature</a>
- Librarian Guides: Share your expertise by writing guides on how to use the Librarian tools.

## Finding Something to Work On
You can find issues to work on
by looking at the <a href={URLS.ISSUES} target="_blank" rel="noreferrer noopener">Issues Board</a> on GitHub
or by joining the <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Hardcover Discord</a> and asking for suggestions in the <a href={URLS.API_DISCORD} target="_blank"
rel="noreferrer noopener">#API</a> or <a href={URLS.LIBRARIAN_DISCORD} target="_blank"
rel="noreferrer noopener">#librarians</a> channels.

## Being a Good Contributor
When contributing to Hardcover, please follow these guidelines:

- Be respectful of others and their contributions.
- Be open to feedback and willing to make changes based on feedback.
- Be patient and understanding of the time it takes to review and merge contributions.
- Be clear and concise in your contributions.
- Be willing to help others and answer questions.
- Be willing to work with others to improve the documentation site.
- Be open to learning and growing as a contributor.
- Be willing to follow the contribution processes.
- Be willing to accept that not all contributions will be accepted.

## How Do I Add a New Page or Update an Existing Page?
### Adding a New Page
1. Navigate to the <a href={URLS.GITHUB} target="_blank" rel="noreferrer noopener">Hardcover Docs GitHub</a>
2. Navigate to the `src/content/docs/` directory.
3. Navigate to the appropriate subdirectory for the page you want to add.
4. Click the "Add file" button near the top right of the file list.
5. Click the "Create new file" option.
6. In the editor that opens, give the new file a meaningful name ending in `.mdx`, see the existing files for examples.
7. Add the [frontmatter](#page-frontmatter) to the new page using the template below.
8. Provide the content for the new page using [Markdown](https://www.markdownguide.org/cheat-sheet/) or [MDX](https://mdxjs.com/guides/) syntax.
9. Preview your changes for formatting and accuracy.
10. Click the "Commit changes..." button at the top of the page.
11. In the dialog that opens, provide a title and description for your changes.
12. Ensure the "Create a new branch for this commit and start a pull request" option is selected.
13. Give your branch a short, descriptive name.
14. Click the "Propose changes" button to save your changes.
15. Notify the Hardcover team, namely `@revelry` in the <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Hardcover Discord</a> that you have submitted a pull request.
16. Wait for feedback and review from the Hardcover team.
17. Make any requested changes.
18. Once your pull request is approved, it will be merged into the main branch.
19. Celebrate your contribution!
20. Continue contributing to Hardcover!

### Editing an Existing Page
1. Using the UI navigate to the page, you want to edit.
2. Click the "Edit page" button near the bottom of the content.
3. In the GitHub page that opens, click the pencil icon on the top right of the file to start editing.
4. Make your changes in the editor using [Markdown](https://www.markdownguide.org/cheat-sheet/) or [MDX](https://mdxjs.com/guides/) syntax.
5. Update the [frontmatter](#page-frontmatter) as needed using the template below, make sure to update the `lastUpdated` field.
6. Preview your changes for formatting and accuracy.
7. Click the "Commit changes..." button at the top of the page.
8. In the dialog that opens, provide a title and description for your changes.
9. Ensure the "Create a new branch for this commit and start a pull request" option is selected.
10. Give your branch a short, descriptive name.
11. Click the "Propose changes" button to save your changes.
12. Notify the Hardcover team, namely `@revelry` in the <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Hardcover Discord</a> that you have submitted a pull request.
13. Wait for feedback and review from the Hardcover team.
14. Make any requested changes.
15. Once your pull request is approved, it will be merged into the main branch.
16. Celebrate your contribution!
17. Continue contributing to Hardcover!

## Adding Images
Currently, images have to be added as a separate pull request. To add an image:

1. Navigate to the <a href={URLS.GITHUB} target="_blank" rel="noreferrer noopener">Hardcover Docs Github</a>
2. Navigate to the `public/images/` directory.
3. Navigate to the appropriate subdirectory `api` or `librarians` depending on where the image will be used.
4. Click the "Add file" button near the top right of the file list.
5. Click the "Upload files" option.
6. Drag and drop the image file(s) into the upload area.
7. In the Commit changes section, provide a title and description for your changes.
8. Ensure the "Create a new branch for this commit and start a pull request" option is selected.
9. Give your branch a short, descriptive name.
10. Click the "Propose changes" button to save your changes.
11. Notify the Hardcover team, namely `@revelry` in the <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Hardcover Discord</a> that you have submitted a pull request.
12. Wait for feedback and review from the Hardcover team.
13. Make any requested changes.
14. Once your pull request is approved, it will be merged into the main branch.
15. After the image is merged, follow the steps in the [Editing an Existing Page](#editing-an-existing-page) section to add the image to and reference it using the relative path: `/images/subdirectory/your-image.png`.

```md
<img src="/images/librarians/long-title-example.png" alt="Example of a long title on Hardcover" />
```

## Page Frontmatter
Moved to [Frontmatter](../frontmatter)

## Available Components
Moved to [Astro Components](../astro-components) for Astro components and [React Components](../react-components) for React components.

## Translation Support
While we currently only support English, we are open to adding translations in the future.
If you are interested in contributing translations,
please reach out to the Hardcover team in the <a href={URLS.API_DISCORD} target="_blank" rel="noreferrer noopener">#API</a>
or <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a> channels on the <a href={URLS.DISCORD} target="_blank"
rel="noreferrer noopener">Hardcover Discord</a>.

## Support Resources

### Finding Help on Discord
Connect with us on <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>
````

## File: src/content/docs/contributing/React-Components.mdx
````
---
title: React Components
category: guide
description: Information about the React components available in the documentation site.
lastUpdated: 2025-03-29 17:10:00
layout: /src/layouts/librarians.astro
---

## Different Types of Components
Currently, there are two types of components available in the documentation site:
- [**Astro Components**](./astro-components): These are components written in Astro and are used to create static HTML pages. Use these components when you don't need any client-side interactivity. Astro components can be used from other Astro components but can not be used from React components.
- [**React Components**](./react-components): These are components written in React and are used to create dynamic, interactive pages. Use these components when you need client-side interactivity or state management. React components can be used from other React components and from Astro components.

## Writing React Components
- React components are written in `.tsx` files in the `/src/components` directory.
- You can use the `useTranslation` and `useTokenTranslation` utility functions from `@/lib/utils` to translate strings in React components.
See [Using Translations in Doc Pages](./using-translations) for more information on how to use translations in React components.

## Available React Components

### UI Components

### Banners
### API Disclaimer Banner

### Librarian Standards Banner



### GraphQL Explorer

These components are planned to be replaced and will be documented at that time.
````

## File: src/content/docs/contributing/Translating-Documentation.mdx
````
---
title: Translating Documentation Guide
category: guide
lastUpdated: 2025-05-02 23:50:00
layout: /src/layouts/librarians.astro
---
import { Steps, Tabs, TabItem } from '@astrojs/starlight/components';

<Tabs>
    <TabItem label="Updating Translations for Existing Pages" default>
        When a page already exists in the translation you are working on, you can update the translation by following these steps:

        <Steps>
            1. Go to the page you want to translate.

            2. Using the language dropdown at the top of the page, select the language you want to translate the document into.

            3. Click the "Edit page" button at the bottom of the page.

            4. Translate the content into the selected language.

            5. After making your changes click the "Commit changes..." button at the top of the page.

            6. In the modal that appears, add a title and description to describe your changes, then click the "Propose changes" button.

            7. In Discord ping `@Revelry` to review your changes.

        </Steps>
    </TabItem>

    <TabItem label="Adding a Page to Existing Translation">
        When browsing the documentation site, you may find a page that is not translated into the language you are viewing.
        If this is the case you might see a banner at the top of the page similar to the one below:

        <img src="/images/Translation-Not-Found-IT.png" alt="Translation Not Found" />

        If you see this banner you will need to create a copy of the page in the translation directory for the language you are viewing,
        and then following the steps outlined in `Updating Translations for Existing Pages`.

        Once a language has been added to the astro config file you can create a new file in the `src/content/docs/` directory
        inside a folder named with the language code. This new file should have the same name as the original file you are translating.

        For example, if you are translating the `src/content/docs/getting-started.mdx` file into Spanish you would create a new
        file at `src/content/docs/es/getting-started.mdx` with the Spanish translation of the content.

        More detailed instructions for how to do this will be added in the future.

    </TabItem>

</Tabs>

## Adding New Languages to the Language Dropdown

If you want to add a new language that is not currently available in the language dropdown,
you can do so by following these steps:

For more information, see [Starlight - Configure i18n](https://starlight.astro.build/guides/i18n/#configure-i18n).

### Important Notes
- The root language should **not** be changed from English.
- When adding a new language, you should also update the existing translation blocks in the astro config file to include the new language.


## How To Reference UI Elements in Translations

Since the Hardcover app is currently only available in English,
you should write the documentation pages with the English labels but also include what the translation should be.

For example, if you are translating a page that references a button with the label "Save",
you should write the page with the button labeled as "Save" and include the translation in the page content like so:

```
Click the <kbd>Save</kbd> button to save your changes.
```

Would become:

```
Haga clic en el botón <kbd>Save</kbd> "Guardar" para guardar los cambios.

```



## Using the New Translations
See [Using Translations in Doc Pages](./using-translations) for more information on how to use the new translations in your documentation pages.
````

## File: src/content/docs/contributing/Using-Translations.mdx
````
---
title: Using Translations in Doc Pages
category: guide
description: Technical documentation on how to use translations in documentation pages.
lastUpdated: 2025-05-02 23:50:00
layout: /src/layouts/librarians.astro
---

This document is relevant when you are building new components or expanding existing ones.
It is not used for translating the documentation pages themselves.

See [Translating Documentation Guide](./translating-documentation) for more information on how to translate documentation pages.

## Using Translations in React Components
When using translations in React components, you can use the `useTranslation` utility function from `@/lib/utils` to translate strings.
This function takes a string as an argument and returns the translated string based on the provided locale.

Currently, translations must be defined in the `src/content/docs/{LANG}/ui.json` file, where `{LANG}` is the language code for the translation.

### Basic Example
```ts
import React from "react";
import { useTranslation } from '@/lib/utils';

const MyComponent = () => {
  return (
    <div>
      <h1>{useTranslation('pages.api.disclaimerBanner.title', locale)}</h1>
    </div>
  );
};
```

### Using Dynamic Tokens
You can also use dynamic tokens in a translation string.<br/>
However, the returned string will need to be sanitized before being rendered.

#### Example
```ts
import {URLS} from "@/Consts";
import {useTokenTranslation} from "@/lib/utils.ts";
import DOMPurify from "dompurify";
import React from "react";

const MyComponent = (locale: string = 'en') => {
    const disclaimerText: string | Node = useTokenTranslation('pages.api.disclaimerBanner.title', locale, {
        "a": (chunks: any) => {
            return `<a href=${URLS.API_DISCORD}
                   target="_blank" rel="noreferrer noopener">{chunks}</a>`
        }
    });

    const sanitizedText = () => ({
        __html: DOMPurify.sanitize(disclaimerText)
    });

    return (
        <div>
            <h1>{sanitizedText()}</h1>
        </div>
    );
};
```
````

## File: src/content/docs/it/api/GraphQL/Schemas/Activities.mdx
````
---
title: Activities
description: Learn about the activities schema in the Hardcover API.
category: reference
lastUpdated: 2024-10-07
layout: /src/layouts/documentation.astro
---

import {Code} from '@astrojs/starlight/components';
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## What is an Activity?

Activities are actions that users perform on the platform.
These actions include things like liking a book, following a user, or adding a book to a shelf.
Activities are used to show what users are doing on the platform and to help users discover new content.

## Types of Activities

There are many types of activities that can be performed on the platform.
Some examples of activities include:

- A user adds a book to a shelf
- A user creates a list
- A user adds a book to a list
- A user reviews a book
- A user marks a book as read
- A user answers a prompt

See some [example payloads below](#example-payloads) for more information on the different types of activities.

## Activity Schema

The activity schema contains the following fields:

### Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>[book](../books)</td>
        <td>Relation</td>
        <td>The book details of the activity</td>
    </tr>
    <tr>
        <td>book_id</td>
        <td>String</td>
        <td>The unique identifier of the book that the activity is related to</td>
    </tr>
    <tr>
        <td>created_at</td>
        <td>String</td>
        <td>The timestamp of when the activity occurred.</td>
    </tr>
    <tr>
        <td>[data](#example-payloads)</td>
        <td>Object</td>
        <td>The payload of the activity</td>
    </tr>
    <tr>
        <td>[event](#event-types)</td>
        <td>String</td>
        <td>The type of activity</td>
    </tr>
    <tr>
        <td>[followers](../users)</td>
        <td>Relation</td>
        <td>List of users who have followed this activity</td>
    </tr>
    <tr>
        <td>id</td>
        <td>String</td>
        <td>The unique identifier of the activity</td>
    </tr>
    <tr>
        <td>[likes](../users)</td>
        <td>Relation</td>
        <td>List of users who have liked this activity</td>
    </tr>
    <tr>
        <td>likes_count</td>
        <td>Number</td>
        <td>The number of users who have liked this activity</td>
    </tr>
    <tr>
        <td>object_type</td>
        <td>String</td>
        <td>'Activity'</td>
    </tr>
    <tr>
        <td>[user](../users)</td>
        <td>Relation</td>
        <td>User object for the user who performed the activity</td>
    </tr>
    <tr>
        <td>user_id</td>
        <td>String</td>
        <td>The unique identifier of the user who performed the activity</td>
    </tr>
    </tbody>
</table>

### Related Schemas
These schemas use the same fields as the activities schema, and are used to help filter and query the activities.

- activity_feed
- activity_foryou_feed

### Event Types
- GoalActivity
- ListActivity
- PromptActivity
- UserBookActivity

### Example Payloads

#### User added a rating to a book
<Code
    code={`
      {
        "id": 3,
        "event": "UserBookActivity",
        "data": {
          "userBook": {
            "rating": "4.5",
            "review": null,
            "statusId": 3,
            "readingFormatId": 1,
            "reviewHasSpoilers": false
          }
        },
        "book_id": 10257,
        "object_type": "Activity"
      }
`}
    lang="graphql"
    title="UserBookActivity"
/>

#### User started reading a book
<Code
    code={`
      {
        "id": 4,
        "event": "UserBookActivity",
        "data": {
          "userBook": {
            "rating": null,
            "review": "",
            "statusId": 1,
            "readingFormatId": 1,
            "reviewHasSpoilers": false
          }
        },
        "book_id": 10257,
        "object_type": "Activity"
      }
`}
    lang="graphql"
    title="User Started Reading"
/>

#### User added a review to a book
<Code
    code={`
    {
        "id": 1234,
        "event": "UserBookActivity",
        "data": {
          "userBook": {
            "rating": "4.5",
            "review": "This is a great book!",
            "statusId": 3,
            "readingFormatId": 1,
            "reviewHasSpoilers": false
          }
        },
        "book_id": 10257,
        "object_type": "Activity"
      }
    }
`}
    lang="graphql"
    title="User Added Review"
/>

#### Goal Activity
<Code
    code={`
    {
        "data": {
          "goal": {
            "id": 12345,
            "goal": 40,
            "metric": "book",
            "endDate": "2024-12-31",
            "progress": 30,
            "startDate": "2024-01-01",
            "conditions": {},
            "description": "2024 Reading Goal",
            "percentComplete": 0.75,
            "privacySettingId": 1
          }
        },
        "event": "GoalActivity",
        "object_type": "Activity"
     },
    }
`}
    lang="graphql"
    title="Goal Activity"
/>

#### List Activity
<Code
    code={`
      {
        "data": {
          "list": {
            "id": 1234,
            "url": null,
            "name": "Owned",
            "path": "@user/lists/owned",
            "ranked": false,
            "featured": false,
            "listBooks": [
              {
                "book": ... See Book schema,
                "position": null,
                "updatedAt": "2024-09-23T23:58:14.027Z"
              }
            ],
            "updatedAt": "2024-09-23T23:58:14.040Z",
            "booksCount": 1,
            "description": "Any editions of books you've marked as 'owned' will show up in this list.",
            "followersCount": 0,
            "privacySettingId": 1
          }
        },
      },
      "event": "ListActivity",
      "object_type": "Activity",
      "book_id": 1108457
    }
}`}
    lang="graphql"
    title="List Activity"
/>

#### Prompt Activity
<Code
    code={`
    {
        "data": {
          "prompt": {
            "id": 1,
            "slug": "what-are-your-favorite-books-of-all-time",
            "user": {
                ... See User schema
            },
            "answers": [{
                "book": ... See Book schema
              }
            ],
            "question": "What are your favorite books of all time?",
            "description": "What are some of your favorites? These can be from any time of your life."
          }
        },
        "event": "PromptActivity",
        "object_type": "Activity",
        "book_id": 370893
    }
`}
    lang="graphql"
    title="Prompt Activity"
/>

## Example Queries

Let's take a look at some example queries that you can use to interact with the activities' schema.

### Get My Activities
<GraphQLExplorer query={`
{
    activities(where: {user_id: {_eq: ##USER_ID##}}, limit: 10) {
        event
        likes_count
        book_id
        created_at
    }
}
`} description={`
    This query will return a list of 10 activities that the current user has performed.
`} presentation='table'/>

### Get Activities for a specific Book
<GraphQLExplorer query={`
{
      activities(
            order_by: {created_at: desc}
            where: {book_id: {_eq: 10257}, event: {_eq: "UserBookActivity"}}
            limit: 10
      ) {
            data
            event
            object_type
            book_id
      }
}
`} description={`
    This query will return a list of 10 activities that have occurred for a specific book.
`}/>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Authors.mdx
````
---
title: Authors
category: reference
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
---


import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Author Schema

The author schema contains the following fields:

### Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>alternate_names</td>
        <td>Array of Strings</td>
        <td>Alternate names for the author</td>
    </tr>
    <tr>
        <td>bio</td>
        <td>String</td>
        <td>The biography of the author</td>
    </tr>
    <tr>
        <td>books_count</td>
        <td>Int</td>
        <td>The number of books the author has contributed to</td>
    </tr>
    <tr>
        <td>born_date</td>
        <td>Date</td>
        <td>The date the author was born</td>
    </tr>
    <tr>
        <td>born_year</td>
        <td>Int</td>
        <td>The year the author was born</td>
    </tr>
    <tr>
        <td>cached_image</td>
        <td>Object</td>
        <td>Metadata for the authors image. This includes the image id, url, primary color, width, and height</td>
    </tr>
    <tr>
        <td>contributions</td>
        <td>[Contribution](../contributions)</td>
        <td>The contributions the author is listed on</td>
    </tr>
    <tr>
        <td>death_date</td>
        <td>Date</td>
        <td>The date the author died</td>
    </tr>
    <tr>
        <td>death_year</td>
        <td>Int</td>
        <td>The year the author died</td>
    </tr>
    <tr>
        <td>id</td>
        <td>String</td>
        <td>The unique identifier of the author</td>
    </tr>
    <tr>
        <td>identifiers</td>
        <td>Array of objects</td>
        <td>IDs for the author on other platforms</td>
    </tr>
    <tr>
        <td>is_bipoc</td>
        <td>Boolean</td>
        <td>Whether the author is Black, Indigenous, or a Person of Color</td>
    </tr>
    <tr>
        <td>is_lgbtq</td>
        <td>Boolean</td>
        <td>Whether the author is LGBTQ+</td>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>The name of the author</td>
    </tr>
    <tr>
        <td>slug</td>
        <td>String</td>
        <td>The Hardcover URL slug</td>
    </tr>
    </tbody>
</table>

## Example Queries

### Get an Author by ID

<GraphQLExplorer query={`
query {
    authors(where: {id: {_eq: "80626"}}, limit: 1) {
        id,
        name
    }
}
`} presentation="table"/>

### Get an Author by Name

<GraphQLExplorer query={`
query {
    authors(where: {name: {_eq: "J.K. Rowling"}}) {
        books_count
        identifiers
        name
    }
}
`} presentation='json' forcePresentation/>

### Get all Authors
<GraphQLExplorer query={`
query {
    authors(limit: 10) {
        id,
        name
    }
}
`} presentation="table"/>

### Get books by an Author
<GraphQLExplorer query={`
query GetBooksByAuthor {
    authors(where: {name: {_eq: "Dan Wells"}}) {
        books_count
        name
        contributions(where: {contributable_type: {_eq: "Book"}}) {
            book {
                title
            }
        }
    }
}
`} description={``} presentation='json' forcePresentation/>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Books.mdx
````
---
title: Books
category: reference
lastUpdated: 2025-03-07 14:20:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>compilation</td>
        <td>bool</td>
        <td></td>
    </tr>
    <tr>
        <td>release_year</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>rating</td>
        <td>float</td>
        <td></td>
    </tr>
    <tr>
        <td>pages</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>users_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>lists_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>ratings_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>reviews_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>author_names</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>cover_color</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>genres</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>moods</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>content_warnings</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>tags</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>series_names</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>has_audiobook</td>
        <td>bool</td>
        <td></td>
    </tr>
    <tr>
        <td>has_ebook</td>
        <td>bool</td>
        <td></td>
    </tr>
    <tr>
        <td>contribution_types</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>slug</td>
        <td>string</td>
        <td></td>
    </tr>
    <tr>
        <td>title</td>
        <td>string</td>
        <td></td>
    </tr>
    <tr>
        <td>description</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>subtitle</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>release_date</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>audio_seconds</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>users_read_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>prompts_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>activities_count</td>
        <td>int32</td>
        <td></td>
    </tr>
    <tr>
        <td>release_date_i</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>featured_series</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>featured_series_position</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>alternative_titles</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>isbns</td>
        <td>string[]</td>
        <td></td>
    </tr>
    <tr>
        <td>contributions</td>
        <td>auto</td>
        <td></td>
    </tr>
    <tr>
        <td>image</td>
        <td>auto</td>
        <td></td>
    </tr>

    </tbody>
</table>


## Get a list of books belonging to the current user

<GraphQLExplorer query={`
{
      list_books(
            where: {
                user_books: {
                    user_id: {_eq: ##USER_ID##}
                }
            },
            distinct_on: book_id
            limit: 5
            offset: 0
      ) {
        book {
              title
              pages
              release_date
        }
      }
}
`} description={`
    This query will return a list of books that the user has added to their collection.
`} presentation='json' forcePresentation/>

## Get a list of books by a specific author

<GraphQLExplorer query={`
query BooksByUserCount {
      books(
            where: {
                contributions: {
                    author: {
                        name: {_eq: "Brandon Sanderson"}
                    }
                }
            }
            limit: 10
            order_by: {users_count: desc}
      ) {
            pages
            title
            id
      }
}
`} description={`
    This query will return a list of the top 10 books by the author Brandon Sanderson, ordered by the number of users who have added the book to their collection.
`} presentation='table'/>

## Getting All Editions of a Book
<GraphQLExplorer query={`
query GetEditionsFromTitle {
    editions(where: {title: {_eq: "Oathbringer"}}) {
        id
        title
        edition_format
        pages
        release_date
        isbn_10
        isbn_13
        publisher {
            name
        }
    }
}
`} description='Get all of the editions for the specific title of `Oathbringer`' presentation='json' forcePresentation/>

## Create a new book
<GraphQLExplorer query={`
mutation {
      createBook(input: {
            title: "My First Book",
            pages: 300,
            release_date: "2024-09-07"
            description: "This is my first book."
        }) {
        book {
              title
              pages
              release_date
              description
        }
      }
}
`} description={`
    This mutation will create a new book with the specified title, number of pages, release date, and description.
`}/>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Characters.mdx
````
---
title: Characters
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Contributions.mdx
````
---
title: Contributions
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Countries.mdx
````
---
title: Countries
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Editions.mdx
````
---
title: Editions
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Goals.mdx
````
---
title: Goals
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Images.mdx
````
---
title: Images
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Languages.mdx
````
---
title: Languages
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Likes.mdx
````
---
title: Likes
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Lists.mdx
````
---
title: Lists
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Notifications.mdx
````
---
title: Notifications
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Platforms.mdx
````
---
title: Platforms
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Prompts.mdx
````
---
title: Prompts
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Publishers.mdx
````
---
title: Publishers
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/ReadingFormats.mdx
````
---
title: Reading Formats
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/ReadingJournals.mdx
````
---
title: Reading Journals
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Recommendations.mdx
````
---
title: Recommendations
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Series.mdx
````
---
title: Series
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Tags.mdx
````
---
title: Tags
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

# Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>

    </tbody>
</table>
````

## File: src/content/docs/it/api/GraphQL/Schemas/Users.mdx
````
---
title: Users
category: reference
lastUpdated: 2024-09-25
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## What is a User?

Users are the people who use the Hardcover platform.
Users can perform actions like adding books to their shelves, following other users, and writing reviews.

## User Schema

The user schema contains the following fields:

### Fields

<table>
    <thead>
    <tr>
        <th>Field</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>String</td>
        <td>The unique identifier of the user</td>
    </tr>
    <tr>
        <td>username</td>
        <td>String</td>
        <td>The username of the user</td>
    </tr>
    <tr>
        <td>birthdate</td>
        <td>String</td>
        <td>The birthdate of the user</td>
    </tr>
    <tr>
        <td>books_count</td>
        <td>Int</td>
        <td>The number of books the user has added</td>
    </tr>
    <tr>
        <td>flair</td>
        <td>String</td>
        <td>The flair of the user</td>
    </tr>
    <tr>
        <td>followers_count</td>
        <td>Int</td>
        <td>The number of followers the user has</td>
    </tr>
    <tr>
        <td>followed_users_count</td>
        <td>Int</td>
        <td>The number of users the user follows</td>
    </tr>
    <tr>
        <td>location</td>
        <td>String</td>
        <td>The location of the user</td>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>The name of the user</td>
    </tr>
    <tr>
        <td>pro</td>
        <td>Boolean</td>
        <td></td>
    </tr>
    <tr>
        <td>pronoun_personal</td>
        <td>String</td>
        <td>The personal pronoun of the user</td>
    </tr>
    <tr>
        <td>pronoun_possessive</td>
        <td>String</td>
        <td>The possessive pronoun of the user</td>
    </tr>
    <tr>
        <td>sign_in_count</td>
        <td>Int</td>
        <td>The number of times the user has signed in</td>
    </tr>
    </tbody>
</table>

## Related Schemas

- me &mdash; The currently authenticated user

## Example Queries

### Get my user information
<GraphQLExplorer query={`
query {
      me {
            id
            username
            birthdate
            books_count
            flair
            followers_count
            followed_users_count
            location
            name
            pro
            pronoun_personal
            pronoun_possessive
            sign_in_count
      }
}`} description={`Get information for the current user`}/>

### Get a User by ID

<GraphQLExplorer query={`
query {
    users(where: {id: {_eq: "1"}}, limit: 1) {
        id,
        username
    }
}
`}/>

### Get a User by Username

<GraphQLExplorer query={`
query {
    users(where: {username: {_eq: "adam"}}, limit: 1) {
        id,
        username
    }
}
`}/>
````

## File: src/content/docs/it/api/guides/GettingAllBooksInLibrary.mdx
````
---
title: Getting All Books in Your Library
category: guide
lastUpdated: 2024-10-07
layout: /src/layouts/documentation.astro
---
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

This guide will show you how to get all the books in your library using the Hardcover API.

## Related Schemas

- [Books](../../api/graphql/schemas/books)

## Get a list of books belonging to the current user

<GraphQLExplorer query={`
{
      list_books(
            where: {
                user_books: {
                    user_id: {_eq: ##USER_ID##}
                }
            },
            distinct_on: book_id
            limit: 5
            offset: 0
      ) {
        book {
              title
              pages
              release_date
        }
      }
}
`} description={`
    This query will return a list of books that the user has added to their collection.
`} presentation='json'/>
````

## File: src/content/docs/it/api/guides/GettingBookDetails.mdx
````
---
title: Getting Book Details
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Related Schemas
- [Books](/api/graphql/schemas/books)
- [Editions](/api/graphql/schemas/editions)

## Getting All Editions of a Book
### Example Request
<GraphQLExplorer query={`
query GetEditionsFromTitle {
    editions(where: {title: {_eq: "Oathbringer"}}) {
        id
        title
        edition_format
        pages
        release_date
        isbn_10
        isbn_13
        publisher {
            name
        }
    }
}
`} description='Get all of the editions for the specific title of `Oathbringer`' presentation='json' forcePresentation />

## Getting Details of a Specific Edition
### Example Request
<GraphQLExplorer query={
`query GetSpecificEdition {
    editions(where: {id: {_eq: 21953653}}) {
        book {
            title
            release_date
            slug
            subtitle
            contributions {
                author {
                    name
                }
            }
        }
    }
}`} description='Get the details of the specific edition of Oathbringer as a physical book published by Tor'/>
````

## File: src/content/docs/it/api/guides/GettingBooksProgress.mdx
````
---
title: Getting Progress of Books
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

### Example Request
<GraphQLExplorer query={``} description='' />
````

## File: src/content/docs/it/api/guides/GettingBooksWithStatus.mdx
````
---
title: Getting Books with a Status
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

This guide will show you how to get books with a specific status.

### Example Request
<GraphQLExplorer query={``} description='' />
````

## File: src/content/docs/it/api/guides/Searching.mdx
````
---
title: Searching for content in the API
description: Search for books, authors, and other content using the Hardcover GraphQL API.
category: guide
lastUpdated: 2024-11-13 21:00:00
layout: /src/layouts/documentation.astro
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## What can I search for?

Currently, you can search for authors, books, characters, lists, prompts, publishers, series, and users.
Additional search options will be added in the future.

## Search options

- `query` - The search term
- `query_type` - The type of content to search for one of (case-insensitive; default `book`)
                    - `author`
                    - `book`
                    - `character`
                    - `list`
                    - `prompt`
                    - `publisher`
                    - `series`
                    - `user`
- `per_page` - The number of results to return per page (default 25)
- `page` - The page number to return (default 1)

## Available fields

- `id`
- `results`

## Example searches

### Authors
When searching authors, we use the following fields:

- `alternate_names` - Alternative names for the author
- `books` - A list of books written by the author
- `name` - The name of the author
- `name_personal` - The personal name of the author
- `series_names` - The names of the different series the author has written

<GraphQLExplorer query={`
    query BooksByRowling {
        search(
            query: "rowling",
            query_type: "Author",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of books written by Rowling.
`} title="Search Authors" presentation='json' forcePresentation/>

### Books
When searching books, we use the following fields:
- `alternative_titles` - Alternative titles for the book
- `author_names` - The name of the authors or contributors of the book
- `isbns` - The ISBNs of the book
- `series_names` - The name of the series the book belongs to
- `title` - The title of the book

<GraphQLExplorer query={`
    query LordOfTheRingsBooks {
        search(
            query: "lord of the rings",
            query_type: "Book",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of books belonging to the Lord of the Rings series.
`} title="Search books" presentation='json' forcePresentation />

### Characters
When searching characters, we use the following fields:

- `author_names` - The name of the author who wrote the books the character appears in
- `books` - A list of books the character appears in
- `name` - The name of the character

<GraphQLExplorer query={`
    query CharactersNamedPeter {
        search(
            query: "peter",
            query_type: "Character",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of characters named Peter.
`} title="Search characters" presentation='json' forcePresentation />

### Lists
When searching lists, we use the following fields:

- `description` - The description of the list
- `books` - A list of books in the list
- `name` - The name of the list

<GraphQLExplorer query={`
    query ListsNamedBest {
        search(
            query: "best",
            query_type: "List",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of lists with the word "best" in the name.
`} title="Search lists" presentation='json' forcePresentation />

### Prompts
When searching prompts, we use the following fields:
- `books` - A list of books for the matching prompt
- `question` - The prompt question

<GraphQLExplorer query={`
    query PromptsAboutLearning {
        search(
            query: "learn from",
            query_type: "Prompt",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of prompts about learning from books.
`} title="Search prompts" presentation='json' forcePresentation />

### Publishers
When searching publishers, we use the following fields:
- `name` - The name of the publisher

<GraphQLExplorer query={`
    query PublishersNamedPenguin {
        search(
            query: "penguin",
            query_type: "Publisher",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of publishers with the word "penguin" in the name.
`} title="Search publishers" presentation='json' forcePresentation />

### Series
When searching series, we use the following fields:
- `author_name` - The name of the author who wrote the series
- `books` - A list of books in the series
- `name` - The name of the series

<GraphQLExplorer query={`
    query SeriesNamedHarryPotter {
        search(
            query: "harry potter",
            query_type: "Series",
            per_page: 7,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of series with the words "harry potter" in the name.
`} title="Search series" presentation='json' forcePresentation />

### Users
When searching users, we use the following fields:
- `location` - The location of the user
- `name` - The name of the user
- `username` - The username of the user

<GraphQLExplorer query={`
    query UsersNamedAdam {
        search(
            query: "adam",
            query_type: "User",
            per_page: 5,
            page: 1
        ) {
            results
        }
    }
`} description={`
    Get a list of users with the name "adam".
`} title="Search users" presentation='json' forcePresentation />
````

## File: src/content/docs/it/api/guides/UpdatingABooksProgress.mdx
````
---
title: Updating a Book's Progress and Dates Read
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
draft: true
---

import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

This guide will show you how to update a book's progress and dates read.

### Example Request
<GraphQLExplorer query={``} description='' />
````

## File: src/content/docs/it/api/guides/UpdatingReadingJournal.mdx
````
---
title: Updating Reading Journal
category: guide
lastUpdated: 2024-12-29 22:49:00
layout: /src/layouts/documentation.astro
draft: true
---
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';

## Introduction

This guide will walk you through how to update a book's reading journal.
This includes updating the progress of the book, the dates read, and the notes you've taken.

### Example Request
<GraphQLExplorer query={``} description='' />
````

## File: src/content/docs/it/api/Getting-Started.mdx
````
---
title: Getting Started with the API
description: Get started with the Hardcover GraphQL API.
category: guide
lastUpdated: 2025-01-02 17:03:00
layout: /src/layouts/documentation.astro
---

import {Badge, Steps} from "@astrojs/starlight/components";
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import { URLS } from "@/Consts";

## Introduction
Our API is accessible using GraphQL. The API that you can use is exactly the same API used by the website, iOS and Android apps.
This means that you can build your own tools and services that interact with the same data that you see on the website.

The API is currently in beta, and we are actively working on it.
We are currently looking for feedback on this API.

### Getting Started Quick Guide
<Steps>
    1. Get your API key
    2. Make your first request
    3. Read the API references and Guides on this site
    4. Build something awesome and share it with us on <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>!
</Steps>

## Getting Help
If you have any questions or need help, please reach out to us on <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>.

## Getting an API Key
To get an API token, you need to go to your account settings page and click on the "Hardcover API" link,
the token will be available at the top of the page.

API tokens are not meant to be shared, and should be kept private, as they can be used to access your account and data.

After you have your token, you can start making requests to the API.

## Making Your First Request
After you have your token, you can head over to the [GraphQL console](https://cloud.hasura.io/public/graphiql?endpoint=https://api.hardcover.app/v1/graphql).
Next, add a header just called "authorization" (no quotes) with your token as the value.

Tab out of the field, and you should see a list of available resources.

### Example Request
To test that it's working, go to the `Try it Yourself` tab below
- Add your token to the `Authorization Token` field.
- Then click the `Run Query` button.

You should see your user ID and username in the Results section.

<GraphQLExplorer query={`
query {
    me {
        id,
        username
    }
}
`}/>

## API Response Codes
The API will return the following response codes:

| Code | Description                                                  | Example Body                                |
|------|--------------------------------------------------------------|---------------------------------------------|
| 200  | The request was successful                                   |                                             |
| 401  | Expired or invalid token                                     | `{ error: "Unable to verify token" }`       |
| 403  | User does not have access to the requested resource or query | `{ error: "Message describing the error" }` |
| 404  | Not Found                                                    |                                             |
| 429  | Too Many Requests, try again later                           | `{ error: "Throttled" }`                    |
| 500  | Internal Server Error                                        | `{ error: "An unknown error occurred" }`    |

## Important Notes About the Hardcover API
- The API is still heavily in flux right now. Anything you build using it could break in the future.
- We may reset tokens without notice while in beta.
- The same ownership rights exist for this as anything on the site.
You own your data.
This means you can't use the API
to access and use someone else's data.
- This API is running the same as if you were using the browser. Any actions you take will be under your user.
- #### <span style="color:red">Don't share your token! Someone could delete your account with it.</span>
- This should only be used from a code backend — never from a browser.
- This is only for offline use at this time.
You can only access this API from localhost or APIs.
Later on, we hope to
allow developers to join a group that allowlists specific sites, but that's a way down the line.

## Limitations
- API tokens automatically expire after 1 year, and reset on January 1st.
- API is rate-limited to 60 requests per minute.
- The following queries are disabled:
    - `_like`
    - `_nlike`
    - `_ilike`
    - `_niregex`
    - `_nregex`
    - `_iregex`
    - `_regex`
    - `_nsimilar`
    - `_similar`
- Queries have a max timeout of 30 seconds.
- Queries are not allowed to run in the browser, they must be run in an environment where the token can be kept secure.
- <Badge text="2025" variant="note" /> Queries have a maximum depth of 3.
- <Badge text="2025" variant="note" /> Queries are limited to your own user data, public data, and user data of users you follow.
- <Badge text="2025" variant="note" /> OAuth support will be added for external applications.

## Want to Contribute?
We are actively looking for contributors to help us improve the API documentation.

For more information about how to contribute to the API Documentation, please see the [Contributing Guide](/contributing/api-docs).

## Further Reading
- [GraphQL API Reference](https://graphql.org/learn/)
````

## File: src/content/docs/it/contributing/API-Docs.mdx
````
---
title: Guida alla Documentazione API
category: guide
lastUpdated: 2025-04-27 13:28:00
layout: /src/layouts/documentation.astro
---
import { FileTree } from '@astrojs/starlight/components';
import { URLS } from "@/Consts";

## FAQ per Sviluppatori

### Come è strutturato il progetto?

#### Struttura dei File

Starlight cerca file `.md` o `.mdx` nella directory `src/content/docs/`.
Ogni file viene esposto come route basata sul nome del file.

Le immagini possono essere aggiunte a `src/assets/` e incorporate nel Markdown con un link relativo.

Gli asset statici, come le favicon, possono essere posizionati nella directory `public/`.

<FileTree>
    - public favicon e altri asset statici
        - ...
    - src
        - assets Immagini per le pagine di documentazione
            - ...
        - components Componenti custom
            - GraphQLExplorer
                - GraphQLExplorer.astro File principale del componente GraphQL Explorer
                - ...
            - ui componenti shadcn/ui
                - ...
            - ...
        - content
            - docs file mdx che generano pagine di documentazione
                - api
                    - GraphQL
                        - Schema Schema dati
                            - ...
                    - ...
                    - guides Guide e tutorial
                        - ...
                    - getting-started.mdx
                    - ...
                - contributing Linee guida per contribuire
                    - ...
                - it Traduzioni in italiano
                    - ...
                -  librarians Guide per bibliotecari
                    - ...
                - ui.json traduzioni per le stringhe UI
        - layouts Layout per pagine di documentazione
            - documentation.astro Layout principale per pagine di documentazione
            - ...
    - astro.config.mjs File di configurazione Astro
    - components.json componenti shadcn/ui
    - CONTRIBUTING Linee guida per contribuire
    - DEVELOPERS.md FAQ per sviluppatori
    - tailwind.config.mjs Configurazione Tailwind CSS
    - ...
</FileTree>


### Come eseguo il progetto in locale?

#### 🚀 Avvio Rapido

1. **Clona il repo:**
```bash
git clone https://github.com/hardcoverapp/hardcover-docs.git
```
2. **Naviga nella directory del progetto:**
```bash
cd hardcover-docs
```
3. **Installa le dipendenze:**
 ```bash
 npm install
  ```
4. **Avvia il dev server:**
 ```bash
 npm run dev
  ```
5. **Apri il browser**
6. **Vai a `http://localhost:4321`**

#### 🧞 Comandi

Il sito di documentazione di Hardcover è costruito con [Astro](https://astro.build/).
Tutti i comandi vengono eseguiti dalla root del progetto, da un terminale:

| Comando                              | Azione                                            |
|:-------------------------------------|:--------------------------------------------------|
| `npm install`                        | Installa le dipendenze                            |
| `npm run dev`                        | Avvia il dev server locale su `localhost:4321` |
| `npm run build`                      | Fai una build di produzione in `./dist/`   |
| `npm run preview`                    | Vedi un'anteprima della build in locale, prima del deploy |
| `npm run astro ...`                  | Esegui comandi CLI come `astro add`, `astro check` |
| `npm run astro -- --help`            | Ottieni aiuto utilizzando la CLI di Astro         |
| `npx vitest`                         | Esegui gli unit tests per il progetto             |
| `npx vitest --coverage.enabled true` | Esegui gli unit test con coverage    |

### Come aggiungo una nuova pagina o aggiorno una pagina esistente?

#### Aggiungere una Nuova Pagina

1. Crea un nuovo file `.mdx` nella directory `src/content/docs/`.
2. Dai al file un nome che descriva il contenuto.
3. Aggiungi il [frontmatter](#page-frontmatter) in cima al file.
4. Aggiungi contenuto al file utilizzando la sintassi Markdown o MDX.
5. Aggiungi la nuova pagina alla barra laterale
 - Se la pagina fa parte delle sezioni `api/GraphQL/Schema` o `guides`, la barra laterale si aggiornerà automaticamente con la nuova pagina.
 - Tutte le altre pagine dovranno essere aggiunte al file di configurazione astro
vedi [Starlight - Aggiungi collegamenti e gruppi di collegamenti](https://starlight.astro.build/it/guides/sidebar/#aggiungi-collegamenti-e-gruppi-di-collegamenti)
per maggiori informazioni.

##### Page Frontmatter
Spostato a [Frontmatter](../frontmatter)

#### Componenti Disponibili
Spostato a [Astro Components](../astro-components) per i componenti Astro e [React Components](../react-components) per i componenti React.

### Tradurre Contenuto
Spostato a to [Translating Documentation Guide](./doc-translations)

## Risorse di Supporto

### Inviare un Bug Report

### Richiedere una Funzionalità

### Trovare Aiuto su Discord
Connettiti con noi su <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>
````

## File: src/content/docs/it/contributing/Astro-Components.mdx
````
---
title: Componenti Astro
category: guide
description: Informazioni sui componenti Astro disponibili nel sito della documentazione.
lastUpdated: 2025-04-28 11:20:00
layout: /src/layouts/librarians.astro
---
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
import SocialIcons from '@/components/SocialIcons.astro';

## Tipi di Componenti
Attualmente, ci sono due tipi di componenti disponibili nel sito dells documentazione:
- [**Componenti Astro**](./astro-components): Questi sono componenti scritti in Astro e vengono utilizzati per creare pagine HTML statiche. Usa questi componenti quando non hai bisogno di interattività lato client. I componenti Astro possono essere utilizzati da altri componenti Astro ma non possono essere utilizzati dai componenti React.
- [**Componenti React**](./react-components): Questi sono componenti scritti in React e vengono utilizzati per creare pagine dinamiche e interattive. Usa questi componenti quando hai bisogno di interattività lato client o gestione dello stato. I componenti React possono essere utilizzati da altri componenti React e da componenti Astro.

## Scrivere Componenti Astro
I componenti Astro vengono scritti in file `.astro` nella directory `/src/components`.

## Componenti Astro Disponibili
Oltre ai componenti standard di [Starlight - Componenti](https://starlight.astro.build/guides/components/), il sito della documentazione di Hardcover include i seguenti componenti personalizzati:

### Explorer GraphQL

Questo componente consente a un utente di visualizzare query GraphQL e sperimentare eseguendole sull'API.

**Percorso di Importazione:**
```js
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
```

**Parametri:**

- `canTry` - Un valore booleano che determina se l'utente può eseguire la query nell'explorer. Il valore predefinito è `true`.
- `description` - Una stringa che descrive la query.
- `forcePresentation` - Un valore booleano che determina se le opzioni di presentazione devono essere nascoste. Il valore predefinito è `false`.
- `presentation` - La presentazione predefinita della risposta, può essere `json` o `table`. Il valore predefinito è `json`.
- `query` - Una stringa contenente la query GraphQL da visualizzare nell'explorer.
- `title` - Una stringa per il titolo della query mostrata nell'explorer. Il valore predefinito è `Example Query`. Modifica questo valore durante la traduzione della pagina in un'altra lingua.

**Utilizzo:**

```mdx
<GraphQLExplorer
    query={query}
    description="Query di esempio"
    presentation='table'
    title="Esempio"
/>
```

<GraphQLExplorer query={`
query {
    me {
        id,
        username
    }
}
`}/>

### Icone Social

Questo componente è principalmente destinato per essere utilizzato internamente, ma può essere utilizzato per visualizzare le icone dei social media di Hardcover.

**Percorso di Importazione:**

```js

import SocialIcons from '@/components/SocialIcons.astro';

```

**Parametri:**

- `iconSize` - Una stringa per la dimensione delle icone. Il valore predefinito è `16px`.

**Utilizzo:**

```mdx
<div class="flex justify-around h-6 w-80">
    <SocialIcons iconSize="20px" />
</div>
```

<div className="flex justify-around h-6 w-80">
    <SocialIcons iconSize="20px" />
</div>

## Limitazioni
- I componenti Astro vengono renderizzati sul server e non hanno accesso agli oggetti `window` o `document` del browser.
- I componenti Astro non supportano la gestione dello stato o l'interattività lato client.
- I componenti Astro non possono essere utilizzati all'interno di componenti React.
````

## File: src/content/docs/it/contributing/Doc-Translations.mdx
````
---
title: Guida alla Traduzione della Documentazione
category: guide
lastUpdated: 2025-04-27 16:59:00
layout: /src/layouts/librarians.astro
---
import { Steps, Tabs, TabItem } from '@astrojs/starlight/components';

<Tabs>
    <TabItem label="Aggiornare le Traduzioni per Pagine Esistenti" default>
        Quando è già presente una traduzione per una pagina, puoi aggiornare la traduzione seguendo questi passaggi:

        <Steps>
            1. Vai alla pagina che desideri tradurre.

            2. Utilizzando il menu delle lingue nella parte superiore della pagina, seleziona la lingua in cui desideri tradurre il documento.

            3. Clicca sul pulsante "Modifica pagina" nella parte inferiore della pagina.

            4. Traduci il contenuto nella lingua selezionata.

            5. Dopo aver apportato le modifiche, clicca sul pulsante "Commit changes..." nella parte superiore della pagina.

            6. Nella finestra modale che appare, aggiungi un titolo e una descrizione per descrivere le tue modifiche, quindi clicca sul pulsante "Propose changes".

            7. Su Discord menziona `@Revelry` per rivedere le tue modifiche.

        </Steps>
    </TabItem>
    <TabItem label="Aggiungere una Pagina a una Traduzione Esistente">
        Durante la navigazione del sito della documentazione, potresti trovare una pagina che non è tradotta nella lingua che stai visualizzando.
        In questo caso potresti vedere un banner nella parte superiore della pagina simile a quello qui sotto:

        <img src="/images/Translation-Not-Found-IT.png" alt="Traduzione Non Trovata" />

        Se vedi questo banner, dovrai creare una copia della pagina nella directory di traduzione per la lingua che stai visualizzando,
        e poi seguire i passaggi descritti in `Aggiornare le Traduzioni per Pagine Esistenti`.

        Una volta che una lingua è stata aggiunta al file di configurazione astro, puoi creare un nuovo file nella directory `src/content/docs/`
        all'interno di una cartella denominata con il codice della lingua. Questo nuovo file deve avere lo stesso nome del file originale che stai traducendo.

        Ad esempio, se stai traducendo il file `src/content/docs/getting-started.mdx` in spagnolo, creeresti un nuovo
        file in `src/content/docs/es/getting-started.mdx` con la traduzione spagnola del contenuto.

        Istruzioni più dettagliate al riguardo saranno aggiunte in futuro.

    </TabItem>

</Tabs>

## Aggiungere nuove lingue al menu delle lingue

Se desideri aggiungere una nuova lingua che non è attualmente disponibile nel menu delle lingue,
puoi farlo seguendo questi passaggi:

Per maggiori informazioni, vedi [Starlight - Configurare i18n](https://starlight.astro.build/it/guides/i18n/#configurare-i18n).

### Note Importanti
- La lingua principale **non** deve essere cambiata dall'inglese.
- Quando aggiungi una nuova lingua, dovresti anche aggiornare i blocchi di traduzione esistenti nel file di configurazione astro per includere la nuova lingua.

## Come fare riferimento agli elementi dell'interfaccia utente nelle traduzioni

Poiché l'app Hardcover è attualmente disponibile solo in inglese,
dovresti scrivere le pagine di documentazione con le etichette in inglese ma includere anche quale dovrebbe essere la traduzione.

Ad esempio, se stai traducendo una pagina che fa riferimento a un pulsante con l'etichetta "Save",
dovresti scrivere la pagina con il pulsante etichettato come "Save" e includere la traduzione nel contenuto della pagina come segue:

```
Click the <kbd>Save</kbd> button to save your changes.
```

Diventerebbe:

```
Clicca sul pulsante <kbd>Save</kbd> "Salva" per salvare le tue modifiche.
```

## Utilizzare le nuove traduzioni
Vedi [Utilizzare le Traduzioni nelle Pagine della Documentazione](./using-translations) per maggiori informazioni su come utilizzare le nuove traduzioni nelle pagine di documentazione.
````

## File: src/content/docs/it/contributing/Frontmatter.mdx
````
---
title: Frontmatter
category: guide
description: Informazioni sul frontmatter utilizzato nelle pagine della documentazione.
lastUpdated: 2025-04-28 13:48:00
layout: /src/layouts/librarians.astro
---

## Cos'è il `Frontmatter`?
Il Frontmatter è un blocco di metadati all'inizio di un file Markdown che fornisce informazioni sulla pagina.
Viene utilizzato da Starlight per generare le pagine HTML e può essere usato per controllare vari aspetti del comportamento e dell'aspetto della pagina.

## Quali opzioni sono disponibili?
Le seguenti opzioni sono disponibili nel frontmatter delle pagine:

Vedi [Starlight -
Frontmatter](https://starlight.astro.build/it/reference/frontmatter/) per ulteriori informazioni e opzioni aggiuntive.

| Campo           | Descrizione                                                                                                                                                                             | Obbligatorio |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| title           | Stringa contenente il titolo della pagina                                                                                                                                               | Sì          |
| category        | Stringa della categoria in cui la pagina deve essere inclusa `guide` o `reference`                                                                                                      | Sì          |
| layout          | Percorso relativo di uno dei layout in `/src/layouts`                                                                                                                                   | Sì          |
| description     | Stringa contenente la descrizione da utilizzare nei meta tag HTML                                                                                                                 | Consigliato |
| lastUpdated     | Stringa nel formato `YYYY-MM-DD HH:MM:SS`                                                                                                                                               | Consigliato |
| draft           | Valore booleano che determina se la pagina debba essere nascosta dal sito di produzione                                                                                                 | No          |
| slug            | Stringa contenente lo slug dell'URL per la pagina                                                                                                                                       | No          |
| tableOfContents | Valore booleano che determina se debba essere generata una tabella dei contenuti                                                                                                        | No          |
| template        | `doc` o `splash` predefinito è `doc`. `splash` è un layout più ampio senza le barre laterali normali                                                                                   | No          |
| hero            | Vedi [Starlight - Frontmatter HeroConfig](https://starlight.astro.build/it/reference/frontmatter/#heroconfig) per ulteriori informazioni                                                   | No          |
| banner          | Vedi [Starlight - Frontmatter Banner](https://starlight.astro.build/reference/frontmatter/#banner) per ulteriori informazioni                                                           | No          |
| prev            | Valore booleano che determina se debba essere mostrato un pulsante di collegamento alla pagina precedente. Vedi [Starlight - Frontmatter Prev](https://starlight.astro.build/it/reference/frontmatter/#prev) per ulteriori informazioni | No          |
| next            | Valore booleano che determina se debba essere mostrato un pulsante di collegamento alla pagina successiva. Vedi [Starlight - Frontmatter Next](https://starlight.astro.build/it/reference/frontmatter/#next) per ulteriori informazioni | No          |
| sidebar         | Controlla come la pagina viene visualizzata nella barra laterale. Vedi [Starlight - Frontmatter Sidebar](https://starlight.astro.build/it/reference/frontmatter/#sidebarconfig) per ulteriori informazioni | No          |


### Esempio di Frontmatter

```md
---
title: Introduzione all'API
description: Inizia a utilizzare l'API GraphQL di Hardcover.
category: guide
lastUpdated: 2025-02-01 17:03:00
layout: ../../layouts/documentation.astro
---
```
````

## File: src/content/docs/it/contributing/Librarian-Guides.mdx
````
---
title: Guida alla Contribuzione per Bibliotecari
category: guide
lastUpdated: 2025-04-27 14:19:00
layout: /src/layouts/librarians.astro
---

import { URLS } from "@/Consts";

# Guida alla Contribuzione per Bibliotecari
## Modi per Contribuire
Attualmente stiamo cercando contributi nelle seguenti aree:

- Documentazione API: Aiutaci a migliorare la documentazione API aggiungendo nuove pagine o aggiornando i contenuti esistenti.
- Guide API: Condividi ciò che conosci scrivendo guide su come utilizzare l'API di Hardcover.
- Correzione Bug: Aiutaci a correggere bug nel sito della documentazione.
- Segnalazione Problemi: Segnala qualsiasi problema riscontrato con il sito della documentazione. <a href={URLS.CREATE_ISSUE} target="_blank" rel="noreferrer noopener">Crea Issue</a>
- Richiesta Funzionalità: Condividi le tue idee per nuove funzionalità o miglioramenti al sito della documentazione. <a href={URLS.SUGGEST_FEATURE} target="_blank" rel="noreferrer noopener">Suggerisci Funzionalità</a>
- Guide per Bibliotecari: Condividi le tue competenze scrivendo guide su come utilizzare gli strumenti per Bibliotecari.

## Trovare Qualcosa su cui Lavorare
Per trovare problemi su cui lavorare puoi guardare la <a href={URLS.ISSUES} target="_blank" rel="noreferrer noopener">Bacheca degli Issues</a> su GitHub
o unirti al <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord di Hardcover</a> e chiedendo suggerimenti nei canali <a href={URLS.API_DISCORD} target="_blank"
rel="noreferrer noopener">#API</a> o <a href={URLS.LIBRARIAN_DISCORD} target="_blank"
rel="noreferrer noopener">#librarians</a>.

## Essere un Buon Contributore
Quando contribuisci a Hardcover, segui queste linee guida:

- Sii rispettoso degli altri e dei loro contributi.
- Sii aperto al feedback e disposto a fare cambiamenti basati sul feedback.
- Sii paziente e comprensivo riguardo al tempo necessario per revisionare e fare merge dei contributi.
- Sii chiaro e conciso nei tuoi contributi.
- Sii disposto ad aiutare gli altri e rispondere alle domande.
- Sii disposto a lavorare con altri per migliorare il sito della documentazione.
- Sii aperto all'apprendimento e alla crescita come contributore.
- Sii disposto a seguire i processi di contribuzione.
- Sii disposto ad accettare che non tutti i contributi saranno accettati.

## Come aggiungo una nuova pagina o aggiorno una pagina esistente?
### Aggiungere una Nuova Pagina
1. Naviga alla pagina <a href={URLS.GITHUB} target="_blank" rel="noreferrer noopener">GitHub della Documentazione di Hardcover</a>
2. Naviga alla directory `src/content/docs/`.
3. Naviga alla sottodirectory della pagina che vuoi aggiungere.
4. Clicca sul pulsante "Add file" nella parte superiore destra dell'elenco dei file.
5. Clicca sull'opzione "Create new file".
6. Nell'editor che si apre, dai al nuovo file un nome significativo che termini con `.mdx`, controlla i file esistenti per vedere degli esempi.
7. Aggiungi il [frontmatter](#page-frontmatter) alla nuova pagina utilizzando il template sottostante.
8. Fornisci il contenuto per la nuova pagina utilizzando la sintassi [Markdown](https://www.markdownguide.org/cheat-sheet/) o [MDX](https://mdxjs.com/guides/).
9. Visualizza un'anteprima delle tue modifiche per verificare formattazione e accuratezza.
10. Clicca sul pulsante "Commit changes..." nella parte superiore della pagina.
11. Nella finestra di dialogo che si apre, fornisci un titolo e una descrizione per le tue modifiche.
12. Assicurati che l'opzione "Create a new branch for this commit and start a pull request" sia selezionata.
13. Dai al tuo branch un nome breve e descrittivo.
14. Clicca sul pulsante "Propose changes" per salvare le tue modifiche.
15. Notifica il team di Hardcover, in particolare `@revelry` nel <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord di Hardcover</a> comunicando che hai inviato una pull request.
16. Attendi una revisione e feedback dal team di Hardcover.
17. Apporta eventuali modifiche richieste.
18. Una volta che la tua pull request è approvata, sarà unita al branch principale.
19. Festeggia il tuo contributo!
20. Continua a contribuire a Hardcover!

### Modificare una Pagina Esistente
1. Utilizzando l'interfaccia utente, naviga alla pagina che desideri modificare.
2. Clicca sul pulsante "Modifica paigina" nella parte inferiore del contenuto.
3. Nella pagina GitHub che si apre, clicca sull'icona della matita nella parte superiore destra del file per iniziare a modificare.
4. Apporta le tue modifiche nell'editor utilizzando la sintassi [Markdown](https://www.markdownguide.org/cheat-sheet/) o [MDX](https://mdxjs.com/guides/).
5. Aggiorna il [frontmatter](#page-frontmatter) utilizzando il modello sottostante, assicurati di aggiornare il campo `lastUpdated`.
6. Visualizza un'anteprima delle tue modifiche per verificare formattazione e accuratezza.
7. Clicca sul pulsante "Commit changes..." nella parte superiore della pagina.
8. Nella finestra di dialogo che si apre, fornisci un titolo e una descrizione per le tue modifiche.
9. Assicurati che l'opzione "Create a new branch for this commit and start a pull request" sia selezionata.
10. Dai al tuo branch un nome breve e descrittivo.
11. Clicca sul pulsante "Propose changes" per salvare le tue modifiche.
12. Notifica il team di Hardcover, in particolare `@revelry` nel <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord di Hardcover</a> comunicando che hai inviato una pull request.
13. Attendi la revisione e feedback dal team di Hardcover.
14. Apporta eventuali modifiche richieste.
15. Una volta che la tua pull request è approvata, sarà unita al branch principale.
16. Festeggia il tuo contributo!
17. Continua a contribuire a Hardcover!

## Aggiungere Immagini
Attualmente, le immagini devono essere aggiunte tramite una pull request separata. Per aggiungere un'immagine:

1. Naviga alla pagine <a href={URLS.GITHUB} target="_blank" rel="noreferrer noopener">GitHub della Documentazione di Hardcover</a>
2. Naviga alla directory `public/images/`.
3. Naviga alla sottodirectory `api` o `librarians` a seconda di dove verrà utilizzata l'immagine.
4. Clicca sul pulsante "Add file" nella parte superiore destra dell'elenco dei file.
5. Clicca sull'opzione "Upload files".
6. Trascina e rilascia i file immagine nell'area di caricamento.
7. Nella sezione Commit changes, fornisci un titolo e una descrizione per le tue modifiche.
8. Assicurati che l'opzione "Create a new branch for this commit and start a pull request" sia selezionata.
9. Dai al tuo branch un nome breve e descrittivo.
10. Clicca sul pulsante "Propose changes" per salvare le tue modifiche.
11. Notifica il team di Hardcover, in particolare `@revelry` nel <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord di Hardcover</a> comunicando che hai inviato una pull request.
12. Attendi la revisione e feedback dal team di Hardcover.
13. Apporta eventuali modifiche richieste.
14. Una volta che la tua pull request è approvata, sarà unita al branch principale.
15. Dopo che l'immagine è stata unita, segui i passaggi nella sezione [Modificare una Pagina Esistente](#editing-an-existing-page) per aggiungere l'immagine e farvi riferimento utilizzando il percorso relativo: `/images/subdirectory/your-image.png`.

```md
<img src="/images/librarians/long-title-example.png" alt="Esempio di un titolo lungo su Hardcover" />
```

## Page Frontmatter
Spostato in [Frontmatter](../frontmatter)

## Componenti Disponibili
Spostato in [Astro Components](../astro-components) per i componenti Astro e [React Components](../react-components) per i componenti React.

## Supporto per le Traduzioni
Sebbene attualmente supportiamo solo l'inglese, siamo aperti ad aggiungere traduzioni in futuro.
Se sei interessato a contribuire con traduzioni,
contatta il team di Hardcover nei canali <a href={URLS.API_DISCORD} target="_blank" rel="noreferrer noopener">#API</a>
o <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a> sul <a href={URLS.DISCORD} target="_blank"
rel="noreferrer noopener">Discord di Hardcover</a>.

## Risorse di Supporto

### Trovare Aiuto su Discord
Connettiti con noi su <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>
````

## File: src/content/docs/it/contributing/React-Components.mdx
````
---
title: Componenti React
category: guide
description: Informazioni sui componenti React disponibili nel sito della documentazione.
lastUpdated: 2025-04-27 17:42:00
layout: /src/layouts/librarians.astro
---

## Tipi di Componenti
Attualmente, ci sono due tipi di componenti disponibili nel sito dells documentazione:
- [**Componenti Astro**](./astro-components): Questi sono componenti scritti in Astro e vengono utilizzati per creare pagine HTML statiche. Usa questi componenti quando non hai bisogno di interattività lato client. I componenti Astro possono essere utilizzati da altri componenti Astro ma non possono essere utilizzati dai componenti React.
- [**Componenti React**](./react-components): Questi sono componenti scritti in React e vengono utilizzati per creare pagine dinamiche e interattive. Usa questi componenti quando hai bisogno di interattività lato client o gestione dello stato. I componenti React possono essere utilizzati da altri componenti React e da componenti Astro.

## Scrivere Componenti React
- I componenti React sono definiti in file `.tsx` nella directory `/src/components`.
- Puoi utilizzare le funzioni utility `useTranslation` e `useTokenTranslation` da `@/lib/utils` per tradurre le stringhe nei componenti React.
Vedi [Utilizzare le Traduzioni nelle Pagine della Documentazione](./using-translations) per maggiori informazioni su come utilizzare le traduzioni nei componenti React.

## Componenti React Disponibili

### Componenti UI

### Banner
### Banner di Disclaimer API

### Banner degli Standard per Bibliotecari

### Esploratore GraphQL

Questi componenti verranno presto sostituiti e saranno documentati in futuro.
````

## File: src/content/docs/it/contributing/Using-Translations.mdx
````
---
title: Utilizzare le Traduzioni nelle Pagine della Documentazione
category: guide
description: Documentazione tecnica su come utilizzare le traduzioni nelle pagine di documentazione.
lastUpdated: 2025-04-28 16:13:00
layout: /src/layouts/librarians.astro
---

Questo documento è rilevante quando stai costruendo nuovi componenti o espandendo quelli esistenti. Non va utilizzato per tradurre le pagine di documentazione.

Vedi [Guida alla Traduzione della Documentazione](./doc-translations) per ulteriori informazioni su come tradurre le pagine di documentazione.

## Utilizzare le Traduzioni nei Componenti React
Quando si utilizzano le traduzioni nei componenti React, puoi utilizzare la funzione utility `useTranslation` da `@/lib/utils` per tradurre le stringhe.
Questa funzione accetta una stringa come argomento e restituisce la stringa tradotta in base alla lingua fornita.

Attualmente, le traduzioni devono essere definite nel file `src/content/docs/{LANG}/ui.json`, dove `{LANG}` è il codice della lingua per la traduzione.

### Esempio Base
```ts
import React from "react";
import { useTranslation } from '@/lib/utils';

const MyComponent = () => {
  return (
    <div>
      <h1>{useTranslation('pages.api.disclaimerBanner.title', locale)}</h1>
    </div>
  );
};
```

### Utilizzare Token Dinamici
Puoi utilizzare anche token dinamici in una stringa di traduzione.<br/>
Tuttavia, la stringa restituita dovrà essere sanitizzata prima di essere renderizzata.

#### Esempio
```ts
import {URLS} from "@/Consts";
import {useTokenTranslation} from "@/lib/utils.ts";
import DOMPurify from "dompurify";
import React from "react";

const MyComponent = (locale: string = 'en') => {
    const disclaimerText: string | Node = useTokenTranslation('pages.api.disclaimerBanner.title', locale, {
        "a": (chunks: any) => {
            return `<a href=${URLS.API_DISCORD}
                   target="_blank" rel="noreferrer noopener">{chunks}</a>`
        }
    });

    const sanitizedText = () => ({
        __html: DOMPurify.sanitize(disclaimerText)
    });
    
    return (
        <div>
            <h1>{sanitizedText()}</h1>
        </div>
    );
};
```
````

## File: src/content/docs/it/librarians/Resources/ISBNAndASIN.mdx
````
---
title: ISBN e ASIN
description: Una panoramica su ISBN e ASIN, e risorse utili.
category: guide
lastUpdated: 2025-03-02 14:05:37
layout: /src/layouts/librarians.astro
---

import {Aside} from "@astrojs/starlight/components";

# Lavorare con l'ISBN

L'**International Standard Book Number** (ISBN) di un libro è un numero univoco
che aiuta a identificare informazioni sulle opere pubblicate. Hardcover estrarrà
automaticamente la maggior parte delle informazioni associate a un ISBN, tuttavia può essere comunque
utile sapere come utilizzare un ISBN per recuperare dati su un'edizione che vuoi aggiungere al database.

**Nota:** Alcuni rivenditori potrebbero fare riferimento a un ISBN come *European Article Number* (EAN).

## Anatomia di un ISBN

Un ISBN è composto da 5 blocchi distinti:

| EAN | Gruppo | Editore | Titolo | Cifra di controllo |
| --- | ----- | --------- | ----- | ----------- |
| 978 | 1     | 9747      | 3463  | 4           |

**EAN**: Quasi sempre 978 o 979.

**Gruppo di registrazione**: Può essere un gruppo di paesi che condividono una lingua, un singolo
paese o territorio.

**Editore**: Un numero univoco assegnato a un editore registrato dalla propria agenzia
locale o nazionale di registrazione ISBN.

**Elemento Titolo / Pubblicazione**: Un numero univoco assegnato dall'editore che è
associato a una specifica edizione di un libro.

**Cifra di controllo**: Un carattere o cifra di checksum, che convalida l'ISBN.

La maggior parte dei blocchi non ha un numero fisso di cifre, rendendo difficile dividere un ISBN nelle sue parti. Tuttavia, gli editori spesso li separano con trattini. Quando aggiungi un ISBN a Hardcover, i trattini vengono rimossi automaticamente.

### Identificare l'editore di un libro

Con l'aiuto dei primi tre blocchi è possibile cercare l'editore di una
specifica edizione. L'International ISBN Agency (Agenzia Internazionale ISBN) mantiene un database aggiornato annualmente e consultabile di tutti gli editori registrati: Il <a href="https://grp.isbn-international.org/" target="_blank" rel="noreferrer noopener">Global Register of Publisher</a> (Registro Globale degli Editori).
Nell'esempio sopra, l'editore registrato per qualsiasi opera che inizia con `978-1-9747` è `Viz Media, Stati Uniti d'America`.

### Identificare una discrepanza tra `Paese`/`ISBN`

Spesso troverai che Hardcover ha estratto l'informazione errata per il campo
`Paese` di un'edizione. Il secondo blocco di un ISBN renderà questo evidente
a colpo d'occhio.

| Gruppo | Regione / Area linguistica / Paese     |
| ----- | ------------------------------------ |
| 0     | Inglese                              |
| 1     | Inglese                              |
| 2     | Francese                             |
| 3     | Tedesco                              |
| 4     | Giappone                             |
| 5     | Ex URSS                              |
| 6     | Prefissi di lunghezza 2 o 3          |
| 7     | Cina                                 |
| 8     | Prefissi di lunghezza 2              |
| 9     | Prefissi di lunghezza 2, 3, 4 o 5    |

*Per un elenco completo, consulta <a href="https://en.wikipedia.org/wiki/List_of_ISBN_registration_groups" target="_blank" rel="noreferrer noopener">Wikipedia</a>*

Se vedi un ISBN `9782820344960` con il `Paese` indicato come `Stati Uniti d'America`, saprai immediatamente che questa edizione necessita di modifiche!

Possiamo anche utilizzare il blocco del gruppo per identificare se un'edizione con un titolo in portoghese è stata pubblicata in Portogallo (972) o in Brasile (85).

## Calcolare ISBN-10 e ISBN-13

I libri pubblicati prima del 2007 molto probabilmente utilizzano un ISBN di dieci cifre. Allo stesso modo,
i libri pubblicati dopo il 2007 spesso non hanno un ISBN-10. È possibile calcolare il
corrispondente ISBN con uno [strumento online](http://www.hahnlibrary.net/libraries/isbncalc.html).

<Aside type="caution">Aggiungere o rimuovere semplicemente ``978`` davanti a un ISBN non produrrà un numero valido! Il blocco di checksum viene calcolato algoritmicamente.</Aside>

## Recuperare informazioni su un libro

L'ISBN non codifica informazioni come il titolo o l'autore di un libro.
Hardcover estrarrà automaticamente questi campi da vari database. Possiamo
verificare questi dati con l'aiuto di alcuni siti web:

* <a href="https://isbnsearch.org" target="_blank" rel="noreferrer noopener">ISBNsearch.org</a>: Controlla rapidamente la rilegatura,
la data di pubblicazione e la copertina associata.
* <a href="https://search.worldcat.org/" target="_blank" rel="noreferrer noopener">WorldCat</a>: WorldCat spesso include descrizioni
fisiche di un libro, incluso il numero di pagine.
* <a href="https://amazon.com" target="_blank" rel="noreferrer noopener">Amazon</a>: La ricerca di un ISBN restituirà la pagina
del prodotto associata al libro. Amazon ha copertine ad alta risoluzione e spesso un
elenco completo di informazioni sulla serie.
* <a href="https://books.google.com" target="_blank" rel="noreferrer noopener">Google Libri</a>: Puoi cercare un libro specifico nel database
di Google aggiungendo `isbn:` davanti all'ISBN. Esempio:
<a href="https://www.google.com/search?udm=36&q=isbn%3A9782820344960" target="_blank" rel="noreferrer noopener">`isbn:9782820344960`</a>.

**Attenzione:** Google tende ad auto-tradurre. Il risultato sopra mostra ``Band 1`` per gli utenti in Germania, ma l'edizione è in realtà francese e dovrebbe essere etichettata come ``Tome 1``!

Infine, puoi cercare informazioni direttamente sul sito web di un editore, che
spesso presenta i dati più accurati e aggiornati.

### Biblioteche Nazionali

Le biblioteche nazionali hanno il compito di preservare documenti e opere pubblicate nei rispettivi paesi. Ciò le rende una buona fonte di informazioni sulle edizioni internazionali di un libro.

| Country | Website                                                                                                                                                    |
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🇦🇺 AU | <a href="https://www.library.gov.au/" target="_blank" rel="noreferrer noopener">National Library of Australia</a>                                          |
| 🇨🇦 CA | <a href="https://library-archives.canada.ca/eng/" target="_blank" rel="noreferrer noopener">Library and Archives Canada</a>                                |
| 🇨🇳 CN | <a href="https://www.nlc.cn/" target="_blank" rel="noreferrer noopener">中国国家图书馆</a>                                                                        |
| 🇫🇷 FR | <a href="https://catalogue.bnf.fr" target="_blank" rel="noreferrer noopener">BnF Catalogue Général</a>                                                     |
| 🇩🇪 DE | <a href="https://katalog.dnb.de/DE/home.html?v=plist" target="_blank" rel="noreferrer noopener">Deutsche National Bibliothek</a>                           |
| 🇬🇧 GB | <a href="https://bll01.primo.exlibrisgroup.com/discovery/search?vid=44BL_INST:BLL01&lang=en" target="_blank" rel="noreferrer noopener">British Library</a> |
| 🇯🇵 JP | <a href="https://www.ndl.go.jp/en/" target="_blank" rel="noreferrer noopener">国立国会図書館</a>                                                                  |
| 🇳🇱 NL | <a href="https://www.kb.nl/en/research-find" target="_blank" rel="noreferrer noopener">Koninklijke Bibliotheek</a>                                         |
| 🇵🇱 PL | <a href="https://www.bn.org.pl/en" target="_blank" rel="noreferrer noopener">Biblioteka Narodowa</a>                                                       |
| 🇵🇹 PT | <a href="https://urn.porbase.org" target="_blank" rel="noreferrer noopener">PORBASE Catalogue</a>                                                          |
| 🇨🇭 CH | <a href="https://www.helveticat.ch" target="_blank" rel="noreferrer noopener">Schweizerische Nationalbibliothek</a>                                        |
| 🇪🇸 ES | <a href="https://www.cultura.gob.es/en/cultura/libro/isbn.html" target="_blank" rel="noreferrer noopener">Ministerio de Cultura de España</a>              |
| 🇮🇹 IT | <a href="https://opac.sbn.it/" target="_blank" rel="noreferrer noopener">Servizio Bibliotecario Nazionale</a>                                              |
| 🇺🇸 US | <a href="https://www.loc.gov/" target="_blank" rel="noreferrer noopener">Library of Congress</a>                                                           |


### Rivenditori

Anche i rivenditori sono una buona fonte di informazioni, ad esempio:

* <a href="https://www.agapea.com/" target="_blank" rel="noreferrer noopener">Agapea</a> (Spagna)
* <a href="https://www.barnesandnoble.com/" target="_blank" rel="noreferrer noopener">Barnes & Noble</a>, <a href="https://www.powells.com/" target="_blank" rel="noreferrer noopener">Powells</a> (Stati Uniti d'America)
* <a href="https://www.cultura.com/" target="_blank" rel="noreferrer noopener">Cultura</a>, <a href="https://www.fnac.com" target="_blank" rel="noreferrer noopener">fnac</a> (Francia)
* <a href="https://www.thalia.de/" target="_blank" rel="noreferrer noopener">Thalia</a>, <a href="https://www.buecher.de/" target="_blank" rel="noreferrer noopener">Bücher.de</a> (Germania)

## ASIN

Amazon utilizza l'**Amazon Standard Identification Number** (ASIN) per l'identificazione
dei prodotti nel loro sistema interno. L'ASIN non è uno standard internazionale. Puoi visualizzare l'ASIN di un libro nella relativa pagina del prodotto sul
sito web di Amazon. Il modo più veloce per trovare l'ASIN è guardare l'URL:

`https://www.amazon.com/dp/0143105434`

L'ASIN di solito segue direttamente dopo `dp`. Per *Wuthering Heights* l'ASIN
è quindi `0141439556`.

**Nota:** Per i libri stampati, l'ISBN-10 è solitamente lo stesso dell'ASIN.

* <a href="https://addons.mozilla.org/en-US/firefox/addon/asin-collector/" target="_blank" rel="noreferrer noopener">ASIN Collector</a> è un'estensione di Firefox che può estrarre in bulk gli ASIN per tutte le edizioni disponibili di un libro.

### ASIN per gli eBook

Per gli eBook l'ASIN di solito inizia con una `B` ed è elencato sotto *Dettagli del prodotto*.

Ad esempio, l'ASIN per *Wuthering Heights - (Penguin Classics Deluxe Edition)* è `B0768ZM5QH`.

<Aside type="caution" title="ISBN per gli eBook">Non farti ingannare da Amazon: una
pagina di prodotto eBook quasi sempre ometterà l'ISBN dell'eBook
in favore di un ASIN. Ciò non significa che l'eBook di *Wuthering Heights* sia
un'esclusiva Kindle. Puoi trovare l'ISBN associato visitando il sito web dell'editore: l'ISBN dell'eBook di 
<a href="https://www.penguinrandomhouse.com/books/286389/wuthering-heights-by-emily-bronte/"
target="_blank" rel="noreferrer noopener">Wuthering Heights</a> è `9780525505143`.</Aside>

## Altri strumenti disponibili

### isbntools
* <a href="https://pypi.org/project/isbntools/" target="_blank" rel="noreferrer noopener">isbntools</a> è un'applicazione CLI Python
in grado di recuperare informazioni ISBN da varie fonti. Può anche elaborare
più ISBN forniti da un file di testo o anche da altri programmi CLI.

Per favore, consulta la documentazione ufficiale per le istruzioni di installazione. Alcuni comandi utili:

```bash
# Ricerca fuzzy di un ISBN dal titolo (conferma sempre il risultato!)
$ isbn_from_words "mistborn final empire"
9780765311788

# Restituisce una raccolta di ISBN associati a un libro
$ isbn_editions 9780765311788
9788413143194
9784150204990
9784150204952

# Ottiene informazioni meta di base
$ isbn_meta 9780765311788
Type:      BOOK
Title:     Mistborn - The Final Empire
Author:    Brandon Sanderson
ISBN:      9780765311788
Year:      2006
Publisher: Macmillan

# Calcola l'ISBN-10
$ to_isbn10 9780765311788
076531178X

# Divide l'ISBN nei suoi elementi
$ isbn_mask 9780765311788
978-0-7653-1178-8

# Usa un servizio e un formato di output specifici
$ isbn_meta 9780525505143 goob json
{"type": "book",
 "title": "Wuthering Heights - (Penguin Classics Deluxe Edition)",
 "author": [{"name": "Emily Bronte"}],
 "year": "2009",
 "identifier": [{"type": "ISBN", "id": "9780525505143"}],
 "publisher": "Penguin"}
```
````

## File: src/content/docs/it/librarians/Standards/AuthorStandards.mdx
````
---
title: Standard per gli autori
description: Standard per aggiungere e modificare autori su Hardcover.
category: guide
lastUpdated: 2025-03-01 12:49:25
layout: /src/layouts/librarians.astro
---

## Nome dell'autore
### Qual è la preferenza per gli autori che usano iniziali doppie nel loro nome? Come "J. R. R. Tolkien" o "J. K. Rowling"?
Alcuni autori usano uno spazio tra le iniziali nel loro nome, altri no. In genere, dovremmo utilizzare il nome ufficiale con cui l'autore si presenta, con la spaziatura che preferisce. Lo slug dell'URL non dovrebbe usare trattini tra le iniziali. Ad esempio "jk-rowling" o "jrr-tolkein".
````

## File: src/content/docs/it/librarians/Standards/BookStandards.mdx
````
---
title: Standard per i libri
description: Standard per aggiungere e modificare libri su Hardcover.
category: guide
lastUpdated: 2025-03-01 14:15:49
layout: /src/layouts/librarians.astro
---

import {Badge} from "@astrojs/starlight/components";

## Titoli
### Quale titolo dovremmo usare per il libro?
Quando possibile, dovremmo usare il titolo ufficiale in inglese con cui il libro è stato pubblicato.

Ad esempio, il titolo originale di "Guerra e Pace" è "Война и миръ". Dovremmo usare "Война и миръ" come titolo dell'edizione russa, ma "War and Peace" come titolo del libro. Questo può essere fatto dalla pagina Edit Book (Modifica Libro) dove sovrascriviamo il titolo dell'edizione. In alternativa, potremmo impostare l'edizione inglese come "Default Physical Edition" (Edizione Fisica Predefinita). Ciò imposterà anche il titolo inglese come titolo.

Se i libri hanno più titoli in inglese (es: "Harry Potter and the Sorcerer's Stone" vs "Harry Potter and the Philosopher's Stone"), dovremmo usare il titolo localizzato per gli USA (Sorcerer's Stone in questo caso).

In futuro, vogliamo permettere alle persone di impostare la loro lingua e far utilizzare automaticamente la versione localizzata, ma per ora puntiamo a usare il titolo USA come predefinito.

### Come gestire invece i libri dei franchise, come "Brotherhood", che fa parte dell'universo di Star Wars?
In questo caso, il titolo ufficiale del libro secondo l'editore è "Star Wars: Brotherhood", e dovremmo usare quello.

In altri casi in cui c'è una serie, dovremmo omettere il nome della serie a meno che non faccia parte del nome (es: Harry Potter and the Sorcerer's Stone). Quando viene omesso (es: The Fellowship of the Ring), dovremmo assicurarci di impostare la serie principale per cui conosciamo questo titolo ("The Lord of the Rings") come serie in evidenza.

### E se il titolo ufficiale include anche la serie?
Questo dipenderà da dove e come la serie fa parte del titolo.

### Come dovremmo gestire i libri con titoli lunghi che contengono i ":" ? Es: "Babel, or The Necessity of Violence: An Arcane History of the Oxford Translators' Revolution"
Imposta il titolo di questo libro su quello dato dall'editore. In questo caso, sarebbe "Babel, or The Necessity of Violence: An Arcane History of the Oxford Translators' Revolution".

Nella pagina del libro, divideremo il titolo per ":" e lo disporremo su più righe se ha un titolo molto lungo.
<img src="/images/librarians/long-title-example.png" alt="Esempio di un titolo lungo su Hardcover" />

Per i libri con un titolo molto lungo, ma un titolo più piccolo e ben noto, dovremmo usare il titolo più breve come slug dell'URL. Questo permette al libro di esistere all'URL https://hardcover.app/books/babel mantenendo un nome più lungo. Gli slug dei libri possono essere modificati solo dalla persona che ha originariamente aggiunto il libro, al moment Adam e Jeff.

### E per il sottotitolo?
Noterai che c'è un campo per il sottotitolo nel modulo di modifica del libro. Attualmente non utilizziamo questo campo per nulla. Ciò che facciamo è dividere il titolo in titolo e sottotitolo quando creiamo i libri. Per esempio:

- Titolo completo: "Wallet Activism: How to Use Every Dollar You Spend, Earn, and Save as a Force for Change".
- Titolo: "Wallet Activism"
- Sottotitolo: "How to Use Every Dollar You Spend, Earn, and Save as a Force for Change"
- Slug: "wallet-activism"

## Descrizioni
### Fonte autorevole per le descrizioni dei libri / Altre informazioni
In ordine di preferenza:

1. Editore
2. Sito web ufficiale dell'autore
3. BookBub / WorldCat
4. Libreria (Barnes & Noble, Amazon, ecc)
5. Altri siti di libri (Open Library, Google Books, ecc)

### Contenuti promozionali / Recensioni / Biografie degli autori / Informazioni sull'edizione nelle descrizioni
Le descrizioni dei libri dovrebbero limitarsi a un'introduzione / riassunto del libro senza spoiler. Le informazioni promozionali aggiuntive dovrebbero essere rimosse, anche se presenti nella descrizione sulla fonte autorevole.

Esempi di contenuti da rimuovere:
    "Dall'autore della serie bestseller xxx"
    "Questo libro è un libro -Autore Famoso"
    "Ristampato per la prima volta in vera pelle"

### Intestazioni delle descrizioni
Se disponibile, usa un'intestazione dell'editore.
Se non viene fornita un'intestazione specifica, ci sono diverse opzioni possibili:

1. Sposta il primo paragrafo della descrizione se è adatto ed è appropriato come elemento autonomo
2. Copia una frase o un'espressione chiave dalla descrizione
3. Lascialo vuoto

## Edizioni predefinite
### Edizione della copertina
Generalmente, l'edizione della copertina dovrebbe essere l'edizione con copertina rigida pubblicata più recentemente del libro con una copertina di qualità "Buona" disponibile; tuttavia, potrebbero esserci casi come stampe speciali o limitate in cui un'altra edizione potrebbe essere più appropriata.
````

## File: src/content/docs/it/librarians/Standards/ComicStandards.mdx
````
---
title: Standard per i fumetti
description: Standard per aggiungere e modificare fumetti su Hardcover.
category: guide
lastUpdated: 2025-03-02 11:56:45
layout: /src/layouts/librarians.astro
---

# Fumetti
## Titolo del Libro
### Numero Singolo

`{Serie} #{Num}: {Titolo}`

   <details>
       <summary>Esempi:</summary>
       The Sandman #1: Sleep of the Just

       Sage #50

       The Amazing Spider-Man #92
   </details>

### Trade Paperbacks (TPB / TP)

`{Serie}, Vol. {num}: {Titolo}`

   <details>
       <summary>Esempi:</summary>
       The Sandman, Vol. 1: Preludes & Nocturnes

       Saga, Vol. 10

       The Amazing Spider-Man, Vol. 5
   </details>

### Altre Collezioni (Copertina Rigida, Omnibus, Libro, ecc)

`{Serie}: {Titolo della Collezione}`

   <details>
       <summary>Esempi:</summary>
       The Sandman: Book One

       Saga: Book Three Deluxe HC

       The Amazing Spider-Man: Omnibus Vol. 1
   </details>

I numeri di uscita / volume non vengono aggiunti agli One Shot / Standalone che non hanno più opere nella serie.

Il titolo è opzionale per i numeri singoli o TPB poiché non tutte le opere li includono, ma in generale dovrebbe seguire come l'editore elenca l'opera. Se un titolo viene utilizzato su un libro, dovrebbe essere incluso per tutti i libri della serie.

Gli anni di pubblicazione non vengono aggiunti ai nomi dei libri a meno che non facciano esplicitamente parte della serie o del titolo dall'editore, poiché queste informazioni sono incluse nel nome della serie visualizzato sopra il libro.

   <details>
       <summary>Esempi:</summary>
       The Amazing Spider-Man (2018) #92 -> The Amazing Spider-Man #92

       Abbott: 1979 -> Abbott: 1979
   </details>

# Serie di Fumetti

## Titoli delle serie

### Numeri

`{Serie} ({Anno})`

   <details>
       <summary>Esempi:</summary>
       Saga

       The Amazing Spider-Man (2018-2022)

       The Amazing Spider-Man (2022-)
   </details>

### Trade Paperbacks

`{Serie} ({Anno}) (TPBs)`

   <details>
       <summary>Esempi:</summary>
       The Sandman (TBPs)

       The Amazing Spider-Man (2012-2022) (TBP)
   </details>

### Altre Collezioni (Copertina Rigida, Omnibus, Libro, ecc)

`{Serie} ({Anno}) (Nome Collezione)`

   <details>
       <summary>Esempi:</summary>
       Saga (Compendiums)
   </details>

La serie "primaria" (cioè il nome della serie senza qualificatori aggiuntivi nel nome e con lo slug più breve) è il formato più regolarmente pubblicato della serie. Per le serie che escono in numeri singoli, questi rappresenterebbero la serie primaria. Se una serie viene pubblicata solo in TPB o Volumi, questa sarebbe la serie primaria.

L'anno è un campo opzionale utilizzato per differenziare diverse pubblicazioni di fumetti sotto lo stesso nome di serie. Gli anni per i nomi delle serie dovrebbero utilizzare l'intervallo completo della serie per le pubblicazioni completate o il primo anno e un trattino per le serie in corso.

   <details>
       <summary>Esempi:</summary>
       Wonder Woman (1987-2006)

       Wonder Woman (2003-)
   </details>

Le collezioni di opere (come i TPB per serie pubblicate come numeri singoli e tutte le altre collezioni) dovrebbero essere contrassegnate come "Compilation" (Raccolta) con i numeri contenuti aggiunti. Le collezioni dovrebbero essere aggiunte come serie "Featured" (In Evidenza) di quel formato di opera, ma non alle serie dei libri che compongono la collezione (ad es., The Sandman: Book Two verrebbe aggiunto come secondo elemento in "The Sandman (Books)" ma non a "The Sandman" o "Vertigo: Winder's Edge").
````

## File: src/content/docs/it/librarians/Standards/EditionStandards.mdx
````
---
title: Standard per le edizioni
description: Standard per aggiungere e modificare edizioni su Hardcover.
category: guide
lastUpdated: 2025-03-02 11:56:45
layout: /src/layouts/librarians.astro
---

import {Badge} from "@astrojs/starlight/components";

## Copertine
### Tipo di file preferito per le immagini di copertina
PNG e JPEG funzionano meglio. I file Webp non sono attualmente supportati. La copertina non dovrebbe avere alcuna trasparenza. L'immagine viene convertita in un file webp prima di essere mostrata, indipendentemente da ciò che carichi.

### Dimensione del file preferita
Più grande è la copertina, meglio è! Se vuoi caricare un file da 15 MB, vai pure. Lo ridimensioneremo e mostreremo una versione più piccola ovunque.

Le copertine che mostriamo su Hardcover (aggiornato al 22 marzo 2024) hanno una dimensione massima di 200px di larghezza per 300px di altezza. Qualsiasi dimensione inferiore a questa mostrerà un'immagine sfocata a causa del ridimensionamento. Qualsiasi copertina che carichi su Hardcover dovrebbe essere almeno 300px di larghezza per 450px di altezza.

### Quali dimensioni sono identificate con rosso, giallo e verde?
Ad oggi mostriamo tre diversi punteggi di qualità per le copertine. Questo viene calcolato usando `altezza x larghezza`.

0 - 32.999: <Badge text="Qualità scarsa" variant="danger" /> (es. 133 x 200)

33.000 - 99.999: <Badge text="Qualità accettabile" variant="caution" /> (es: 200 x 300)

100.000 +: <Badge text="Buona qualità" variant="success" /> (es: 300 x 450)

Vorremmo iniziare a mostrare copertine più grandi nella pagina del libro, il che richiederà più copertine nel range di Qualità eccellente.

## Collaboratori
### Ordine di elenco dei collaboratori dell'edizione
Aggiungi gli autori principali nello stesso ordine in cui appaiono sulla copertina del libro. I collaboratori aggiuntivi (editori, illustratori, ecc.) possono essere aggiunti in qualsiasi ordine.

### Antologie con più autori
Per opere contenenti numerosi autori, come antologie di racconti brevi, tutti gli autori contributori dovrebbero essere elencati con il ruolo di autore.

   <details>
       <summary>Esempi:</summary>
       Unbound, pubblicato da Grim Oak Press mostra l'Autore come "Multiple" (Multipli) ed elenca gli Autori e le loro contribuzioni nella descrizione.

       In questo caso, tutti i 23 autori contributori dovrebbero essere elencati come Autore dell'edizione.
   </details>

## Informazioni di pubblicazione
### Nome dell'editore
Elenca il nome dell'azienda che ha pubblicato questa edizione.

Gli autori che si autopubblicano sotto il proprio nome dovrebbero essere inseriti come "Independently Published" (Pubblicato in modo indipendente). Le piccole aziende, incluse le LLC stabilite dall'autore che pubblicano solo le opere di quell'autore, hanno comunque elencato il nome dell'azienda.

Non includere virgole o punti intorno agli acronimi di entità commerciali.

   <details>
       <summary>Esempi:</summary>
       Julie Carobini -> Pubblicato in modo indipendente

       Julie Carobini, LLC -> Julie Carobini LLC

       Julie Carobini Inc. -> Julie Carobini Inc
   </details>

### Data di pubblicazione
Elenca la data di pubblicazione dell'edizione fornita dall'editore. È importante che almeno un'edizione di un libro abbia una data di pubblicazione valida per la corretta visualizzazione del libro nelle serie o in altri luoghi. Hardcover selezionerà automaticamente la data di pubblicazione più antica da visualizzare sulla pagina libro.

Se non esiste una data specifica di pubblicazione o non si trova, elenca la data come 1 gennaio di quell'anno. Se è disponibile il mese ma non il giorno, elencalo come il primo giorno di quel mese: 1/1/anno
````

## File: src/content/docs/it/librarians/Standards/SeriesStandards.mdx
````
---
title: Standard per le serie
description: Standard per aggiungere e modificare serie su Hardcover.
category: guide
lastUpdated: 2025-03-01 12:49:25
layout: /src/layouts/librarians.astro
---

## Nomi di serie duplicati
Per più serie con lo stesso nome, modifica le serie aggiuntive come segue:
  - Aggiungi `(Nome Autore)` al nome della serie
  - Aggiungi `-NomeAutore` allo slug

Quando una serie è stata adattata in un formato diverso (ad esempio, un manga che è stato adattato a romanzo), creiamo una serie separata per l'adattamento:
  - Il formato originale mantiene il nome della serie (ad esempio, `L'estate in cui Hikaru è morto`)
  - Per l'adattamento, aggiungi `(Formato)` al nome della serie (ad esempio, `L'estate in cui Hikaru è morto (Light Novel)`)
  - Per l'adattamento, aggiungi `-formato` allo slug (ad esempio, `l-estate-in-cui-hikaru-e-morto-lightnovel`)

## Collezioni editoriali (ad esempio, Penguin Little Black Classics)
Per collezioni editoriali o altre collezioni dove solo un'edizione specifica di un libro fa parte della serie, non va creata una serie su Hardcover. Il libro può essere invece aggiunto a una lista.
````

## File: src/content/docs/it/librarians/Editing.mdx
````
---
title: FAQ Modifiche
description: Domande frequenti sulla modifica di libri / edizioni.
category: guide
lastUpdated: 2025-03-02 19:57:15
layout: /src/layouts/librarians.astro
---

## Generale
### Come posso aggiungere un libro se non lo trovo su Hardcover?
Se cerchi un libro e non lo vedi nei risultati, vai alla pagina Add Book to Hardcover (Aggiungi Libro a Hardcover). Lì puoi aggiungere un libro tramite ISBN 10, ISBN 13 o Goodreads ID. Questo è il miglior modo per iniziare, poiché è possibile che il libro non appaia nella ricerca per vari motivi (principalmente perché la cache di ricerca è obsoleta, o questo libro è stato aggiunto manualmente da un utente di recente e non è  stato ancora approvato).

Se questo libro non ha un ISBN e non è su Goodreads, allora puoi utilizzare il modulo New Edition (Nuova Edizione). Questo creerà un nuovo libro con questa come unica nuova edizione. Quando i bibliotecari aggiungono libri usando questo modulo, questi appariranno subito per tutti. Quando ospiti e non-bibliotecari aggiungono libri usando questo modulo, a quei libri verrà assegnato un valore "aggiunto dall'utente" dietro le quinte che impedisce che appaiano nella ricerca.

### Come posso unire i libri?
Nella pagina del libro, clicca sul pulsante <kbd>Flag</kbd> (Segnala) e dal menu a discesa seleziona <kbd>Mark as Duplicate</kbd> (Segna come Duplicato). Questo aprirà una modale (o un overlay su mobile) che ti permetterà di cercare e selezionare di quale libro l'attuale libro è un duplicato. Seleziona quel libro e clicca sul pulsante per segnalarlo come duplicato.

Se hai un livello di accesso superiore all'impatto che l'unione dei libri comporterebbe, i libri verranno uniti immediatamente. Se cerchi di unire un libro popolare con un altro libro, un amministratore riceverà la richiesta di unione per controllarla prima di eseguirla. Una volta eseguita, riceverai una notifica.

### Quando si combinano libri/serie/autori duplicati, quale versione dovrei mantenere?
Nel caso di autori, serie e personaggi, mantieni quello con il nome canonico inglese.

Per i libri, scegli quello con il maggior numero di lettori. Quando un altro lettore seleziona quel libro da leggere, l'"edizione" che il lettore ha letto sarà per impostazione predefinita l'edizione principale di questo libro. Selezionare il libro con più lettori fa in modo che le prossime persone che lo leggeranno saranno assegnate alla stessa edizione popolare.

### La copertina del libro è sfocata anche se l'edizione ha un'immagine ad alta risoluzione
Verifica che il file non sia un webp (a volte i file webp provenienti da editori o autori sono erroneamente contrassegnati con l'estensione .jpg). In questo caso puoi risalvarlo con qualsiasi editor di immagini per convertirlo in un reale jpg o png prima di caricarlo su Hardcover.

## Edizioni
### Un ISBN è già erroneamente in uso su un'altra edizione
Rimuovi l'ISBN dal libro sbagliato usando il pulsante <kbd>Hard Reset</kbd>, quindi aggiungilo all'edizione corretta.

### Qual è la differenza tra 'Edition Format' (Formato Edizione) e 'Reading Format' (Formato di Lettura) quando si modifica un libro?
Nel modulo di modifica dell'edizione chiediamo entrambi, ma solo "Reading Format" è obbligatorio. Il formato di lettura ha tre opzioni: <kbd>Audiobook</kbd> (Audiolibro), <kbd>Physical Book</kbd> (Libro fisico) e <kbd>Ebook</kbd>.

<kbd>Edition Format</kbd> è un campo di testo utilizzato per aggiungere dettagli su questa specifica edizione. Ad esempio: <kbd>Hardcover</kbd> (Copertina rigida), <kbd>Mass market paperback</kbd> (Tascabile), <kbd>Full cast audiobook</kbd> (Audiolibro con cast completo), <kbd>Kickstarter Version</kbd> (Versione Kickstarter), ecc.

Questo rappresenta quella specifica edizione del libro, non da dove l'hai letto. È improbabile che si inserisca <kbd>Kindle Edition</kbd> (Edizione Kindle), a meno che questa edizione non sia stata originariamente creata per Kindle e sia diversa da altre versioni.

Nella maggior parte dei casi, oppure se hai dubbi, puoi lasciare questo campo vuoto.

## Serie
### Il conteggio dei libri della serie è basso o nelle pagine di autori/libri mancano le miniature delle serie
Il conteggio dei libri della serie e le anteprime della serie considerano solo i libri con una data di pubblicazione. Verifica che almeno un'edizione per tutti i libri della serie abbia una data di pubblicazione valida.

## Altro
### Il mio aggiornamento non ha funzionato. Cosa sta succedendo?
Se riscontri un bug, avvia una discussione nel canale bugs and questions (bug e domande) con più informazioni possibili per aiutare a riprodurre l'errore (link alla pagina che stavi modificando, quali campi hai modificato).
````

## File: src/content/docs/it/librarians/FAQ.mdx
````
---
title: FAQ Bibliotecari
description: Domande frequenti per i bibliotecari.
category: guide
lastUpdated: 2025-03-01 11:56:15
layout: /src/layouts/librarians.astro
---

import { URLS } from "@/Consts";

## Generale
### Come posso avere aiuto come bibliotecario quando ho una domanda?
Primo passo: questo documento! Leggilo e verifica se c'è una risposta alla tua domanda.

Se non trovi risposta, unisciti al nostro <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>. Non preoccuparti, non è necessario essere esperti di Discord. Lo utilizziamo principalmente come chat di gruppo per le persone su Hardcover, con alcuni canali speciali per Librarians (Bibliotecari) e Supporters (Sostenitori). Una volta iscritto a Discord, dovrai collegare Discord con il tuo account Hardcover per accedere al canale <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a>. Puoi seguire le istruzioni in questo articolo per aggiungere il ruolo “librarian” (o “supporter”), che ti garantirà l'accesso.

### Se sei un bibliotecario approvato, puoi diventare anche un sostenitore?
Sì, per favore fallo: Hardcover sarebbe felice di avere il tuo supporto! I sostenitori mantengono tutti i permessi di modifica di un bibliotecario, ma ottengono anche alcuni vantaggi extra.

## Accesso

### Come si diventa bibliotecari?
{URLS.LIBRARIAN_APPLICATION}

### Come posso unirmi al Discord di Hardcover per Bibliotecari?
Le istruzioni sono [qui](https://hardcover.app/pages/how-to-link-hardcover-roles-with-discord).

## Privilegi

### Quali privilegi ottengono i bibliotecari?
I bibliotecari possono modificare la maggior parte dei campi di libri, edizioni e autori. In futuro, i bibliotecari potranno anche modificare serie, personaggi e altri dati relativi ai libri.

### Quali privilegi ottengono i sostenitori?
I sostenitori ottengono gli stessi permessi di modifica dei bibliotecari finché rimangono sostenitori. I sostenitori ottengono anche benefici aggiuntivi sul sito, come il flair Supporter e l'accesso anticipato all'ambiente di staging per fornire feedback e contribuire a plasmare il futuro di Hardcover.

### Cosa impedisce a un bibliotecario di danneggiare un libro/autore/ecc?
Per libri/edizioni con un "punteggio" elevato, generalmente qualsiasi cosa con cinque o più letture, esiste un controllo che invia modifiche significative, come fusioni o cancellazioni, alla coda del bibliotecario capo per l'approvazione prima che la modifica venga applicata.
Detto questo, i bibliotecari hanno molto potere, se non sei mai sicuro di un'azione che stai per eseguire, chiedi prima!

## Bug e Problemi
### Come posso segnalare un bug?
Innanzitutto, mi dispiace che tu abbia riscontrato un bug. Abbiamo cercato di muoverci il più velocemente possibile, e questo ha significato tenere molti piatti in equilibrio. A volte cadono e dobbiamo sistemare le cose. 😅

Entra su <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a> e unisciti al canale <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a>. Pubblica lì informazioni su eventuali bug che stai riscontrando.
````

## File: src/content/docs/it/librarians/Getting-Started.mdx
````
---
title: Getting Started as a librarian
description: Get started contributing to Hardcover as a librarian.
category: guide
lastUpdated: 2025-01-03 19:42:00
layout: /src/layouts/librarians.astro
draft: true
---

import { URLS } from "@/Consts";

Please check out the FAQ for information on how to get started as a librarian.
If you have any questions, please reach out to us on <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>.
````

## File: src/content/docs/it/404.mdx
````
---
title: '404'
template: splash
editUrl: false
hero:
    title: '404'
    tagline: La pagina richiesta non è stata trovata. Controlla l'URL o prova a utilizzare la barra di ricerca sopra oppure una delle opzioni qui sotto.
---

import { LinkCard } from '@astrojs/starlight/components';
import { URLS } from '@/Consts';


<LinkCard title="Homepage della documentazione"
          description="Torna alla pagina principale della documentazione"
          href="/"
/>
<LinkCard title="App Hardcover"
          description="Vai all'app Hardcover"
          href={URLS.APP}
          target="_blank"
/>
````

## File: src/content/docs/it/index.mdx
````
---
title: Benvenuti alla documentazione di Hardcover!
description: Inizia a contribuire a Hardcover
template: splash
hero:
    title: Benvenuti alla documentazione di Hardcover!
    tagline: Inizia a contribuire a Hardcover
    image:
        file: /src/assets/hardcover.svg
        alt: Logo di Hardcover
    actions:
        - text: Documentazione API
          link: ./api/getting-started
          variant: primary
        - text: Guide per Bibliotecari
          link: ./librarians/faq
          variant: primary
---

import { LinkCard } from '@astrojs/starlight/components';
import { URLS } from '@/Consts';

<LinkCard title="Ritorna all'app Hardcover" href={URLS.APP} target="_blank" rel="noreferrer noopener" />
````

## File: src/content/docs/it/ui.json
````json
{
  "lang": {
    "label": "Italiano",
    "code": "it"
  },
  "pages": {
    "api": {
      "disclaimerBanner": {
        "title": "Avviso",
        "text": "Questa API è attualmente in fase di sviluppo e potrebbe cambiare o non funzionare in qualsiasi momento senza preavviso. Se hai domande o hai bisogno di aiuto, chiedi pure nel canale Discord <a>#api</a>."
      }
    },
    "librarians": {
      "standardsBanner": {
        "title": "Nota",
        "text": "Le regole e le linee guida incluse nelle sezioni degli standard di questa documentazione hanno lo scopo di fornire un quadro generale per guidare i nuovi bibliotecari, offrire esempi su come gestire scenari comuni di modifica e presentare coerenza in tutto il sito. Ciò detto, i libri non sono tutti uguali, quindi è impossibile che un singolo standard sia perfettamente applicabile in tutte le situazioni. Se ritieni che un'opera in particolare non rientri in questi standard o hai suggerimenti per miglioramenti, faccelo sapere nel canale Discord <a>#librarians</a>."
      }
    }
  },
  "sidebar": {
    "api": {
      "title": "Documentazione API",
      "gettingStarted": "Primi Passi",
      "guides": "Guide",
      "schemas": "Schemi"
    },
    "contributing": {
      "title": "Guide alla Contribuzione"
    },
    "librarians": {
      "title": "Guide per Bibliotecari",
      "editing": "FAQ Modifiche",
      "faq": "FAQ Bibliotecari",
      "gettingStarted": "Primi Passi come Bibliotecario",
      "resources": "Risorse",
      "standards": "Standard"
    }
  },
  "site": {
    "title": "Hardcover"
  },
  "ui": {
    "lastUpdated": "Ultimo Aggiornamento",
    "graphQLExplorer": {
        "query": "Query",
        "example": "Query di esempio",
        "viewQuery": "Visualizza query",
        "results": "Risultati",
        "tryIt": "Provalo tu stesso",
        "authToken": "Token di Autorizzazione",
        "authTokenDescription": "Questo token verrà utilizzato per autenticare le tue richieste. Puoi trovarlo nelle impostazioni del tuo account.",
        "run": "Esegui query",
        "runDescription": "Esegui la query mostrata qui di seguito",
        "views": {
           "default": "Vista predefinita",
           "chart": "Vista grafico",
           "json": "Vista JSON",
           "table": "Vista tabella"
        },
        "statusMessages": {
           "warning": "Attenzione!",
           "disclaimer": "Questa query verrà eseguita sul tuo account. Sei responsabile del contenuto di qualsiasi query eseguita sul tuo account.",
           "loading": "Caricamento...",
           "error": "Errore",
           "errorRunning": "Errore durante l'esecuzione della query",
           "connectionError": "Errore di connessione al server",
           "emptyQuery": "Nessuna query fornita",
           "mutationQueryNotAllowed": "Le mutazioni non sono attualmente consentite in questo explorer",
           "invalidQuery": "Query non valida",
           "emptyToken": "Nessun token di autenticazione fornito",
           "invalidToken": "Token di autenticazione non valido o scaduto",
           "success": "Successo!",
           "noResults": "Nessun risultato trovato",
           "viewUnavailable": "Questa vista non è disponibile per i risultati di questa query."
        
       }
    }
  }
}
````

## File: src/content/docs/librarians/Resources/ISBNAndASIN.mdx
````
---
title: ISBN and ASIN
description: An overview of ISBN and ASIN, along with helpful resources.
category: guide
lastUpdated: 2025-07-27 14:00:00
layout: /src/layouts/librarians.astro
---

import {Aside} from "@astrojs/starlight/components";

# Working with ISBN

The **International Standard Book Number** (ISBN) of a book is a unique number
which helps identify information about published works. While Hardcover will
pull most information associated with an ISBN automatically, it can still be
helpful to know how to use an ISBN to retrieve data about an edition you're
intending to add to the database.

**Note:** Some retailers may refer to an ISBN as *European Article Number* (EAN).

## Dissecting an ISBN

An ISBN consists of 5 distinct blocks:

| EAN | Group | Publisher | Title | Check digit |
| --- | ----- | --------- | ----- | ----------- |
| 978 | 1     | 9747      | 3463  | 4           |

**EAN Prefix**: Almost always 978 or 979.

**Registration Group**: Either a language-sharing country group, individual
country or territory.

**Publisher**: A unique number issued to a registered publisher by their local
or national ISBN registration agency.

**Title / Publication Element**: A unique number assigned by the publisher which is
associated with a specific edition of a book.

**Check digit**: A checksum character or digit, validating the ISBN.

Most blocks do not have a fixed number of digits, making it difficult to split an ISBN into its parts. However, publishers often separate them with hyphens. When you add an ISBN to Hardcover, the hyphens are automatically removed.

### Identifying the publisher of a book

With the help of the first three blocks it is possible to look up the publisher of a
specific edition. The International ISBN Agency maintains an annually updated and searchable database of all registered publishers: The <a href="https://grp.isbn-international.org/" target="_blank" rel="noreferrer noopener">Global Register of Publishers</a>.
In the example above the registered publisher for any works starting with `978-1-9747` is `Viz Media, United States of America`.

### Identifying a `Country`/`ISBN` mismatch

You will often find that Hardcover has pulled the wrong information for the
`Country` field of an edition. The second block of an ISBN will make that obvious
at a glance. 

| Group | Region / Language Area / Country     |
| ----- | ------------------------------------ |
| 0     | English                              |
| 1     | English                              |
| 2     | French                               |
| 3     | German                               |
| 4     | Japan                                |
| 5     | Former USSR                          |
| 6     | Prefixes of length 2 or 3            |
| 7     | China                                |
| 8     | Prefixes of length 2                 |
| 9     | Prefixes of length 2, 3, 4 or 5      |

*For a complete list, refer to <a href="https://en.wikipedia.org/wiki/List_of_ISBN_registration_groups" target="_blank" rel="noreferrer noopener">Wikipedia</a>*

If you see ISBN `9782820344960` with the `Country` listed as `United States of
America` you will immediately know that this edition needs editing!

We can also use the group block to identify whether an edition with a Portuguese title was published in Portugal (972) or Brazil (85).

## Calculating ISBN-10 and ISBN-13

Books published before 2007 will most likely use a ten-digit long ISBN. Similarly,
books published after 2007 often lack an ISBN-10. You can calculate the
corresponding ISBN with an [online
tool](http://www.hahnlibrary.net/libraries/isbncalc.html) ([alternate](https://isbn.co.in/check-digit/)).

<Aside type="caution">Simply adding or removing ``978`` in
front of an ISBN will not result in a valid number! The checksum block is algorithmically calculated.</Aside>

## Retrieving information about a book

The ISBN does not encode information such as title or author of a book.
Hardcover will pull these fields from various databases automatically. We can
verify this data with the help of a few websites:

* <a href="https://isbnsearch.org" target="_blank" rel="noreferrer noopener">ISBNsearch.org</a>: Quickly check the binding,
publication date and associated cover.
* <a href="https://search.worldcat.org/" target="_blank" rel="noreferrer noopener">WorldCat</a>: WorldCat will often include physical
descriptions of a book, including the page count.
* <a href="https://amazon.com" target="_blank" rel="noreferrer noopener">Amazon</a>: Searching for an ISBN will return the product
page associated with the book. Amazon has high resolution covers and often a
complete list of series information.
* <a href="https://books.google.com" target="_blank" rel="noreferrer noopener">Google Books</a>: You can search through Google's
database for a specific book by appending `isbn:` in front of the ISBN. Example:
<a href="https://www.google.com/search?udm=36&q=isbn%3A9782820344960" target="_blank" rel="noreferrer noopener">`isbn:9782820344960`</a>. 

**Careful:** Google tends to auto-translate. The result above shows ``Band 1`` for users in Germany, but the edition is actually from France and should be labeled as ``Tome 1``!

Finally, you can look up information directly on a publisher's website, which
will often feature the most accurate and up-to-date data.

### National Libraries

National libraries are tasked with the preservation of documents and works published in their respective countries. This makes them a good source of information about international editions of a book.

| Country | Website                                                                                                                                                    |
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🇦🇺 AU | <a href="https://www.library.gov.au/" target="_blank" rel="noreferrer noopener">National Library of Australia</a>                                          |
| 🇨🇦 CA | <a href="https://library-archives.canada.ca/eng/" target="_blank" rel="noreferrer noopener">Library and Archives Canada</a>                                |
| 🇨🇳 CN | <a href="https://www.nlc.cn/" target="_blank" rel="noreferrer noopener">中国国家图书馆</a>                                                                        |
| 🇫🇷 FR | <a href="https://catalogue.bnf.fr" target="_blank" rel="noreferrer noopener">BnF Catalogue Général</a>                                                     |
| 🇩🇪 DE | <a href="https://katalog.dnb.de/DE/home.html?v=plist" target="_blank" rel="noreferrer noopener">Deutsche National Bibliothek</a>                           |
| 🇬🇧 GB | <a href="https://bll01.primo.exlibrisgroup.com/discovery/search?vid=44BL_INST:BLL01&lang=en" target="_blank" rel="noreferrer noopener">British Library</a> |
| 🇯🇵 JP | <a href="https://www.ndl.go.jp/en/" target="_blank" rel="noreferrer noopener">国立国会図書館</a>                                                                  |
| 🇳🇱 NL | <a href="https://www.kb.nl/en/research-find" target="_blank" rel="noreferrer noopener">Koninklijke Bibliotheek</a>                                         |
| 🇵🇱 PL | <a href="https://www.bn.org.pl/en" target="_blank" rel="noreferrer noopener">Biblioteka Narodowa</a>                                                       |
| 🇵🇹 PT | <a href="https://urn.porbase.org" target="_blank" rel="noreferrer noopener">PORBASE Catalogue</a>                                                          |
| 🇨🇭 CH | <a href="https://www.helveticat.ch" target="_blank" rel="noreferrer noopener">Schweizerische Nationalbibliothek</a>                                        |
| 🇪🇸 ES | <a href="https://www.cultura.gob.es/en/cultura/libro/isbn.html" target="_blank" rel="noreferrer noopener">Ministerio de Cultura de España</a>              |
| 🇮🇹 IT | <a href="https://opac.sbn.it/" target="_blank" rel="noreferrer noopener">Servizio Bibliotecario Nazionale</a>                                              |
| 🇺🇸 US | <a href="https://www.loc.gov/" target="_blank" rel="noreferrer noopener">Library of Congress</a>                                                           |


### Retailers

Retailers are also a good source for information, for example:

* <a href="https://www.agapea.com/" target="_blank" rel="noreferrer noopener">Agapea</a> (Spain)
* <a href="https://www.barnesandnoble.com/" target="_blank" rel="noreferrer noopener">Barnes & Noble</a>, <a href="https://www.powells.com/" target="_blank" rel="noreferrer noopener">Powells</a> (United States of America)
* <a href="https://www.cultura.com/" target="_blank" rel="noreferrer noopener">Cultura</a>, <a href="https://www.fnac.com" target="_blank" rel="noreferrer noopener">fnac</a> (France)
* <a href="https://www.thalia.de/" target="_blank" rel="noreferrer noopener">Thalia</a>, <a href="https://www.buecher.de/" target="_blank" rel="noreferrer noopener">Bücher.de</a> (Germany)

## ASIN

Amazon uses the **Amazon Standard Identification Number** (ASIN) for product
identification within their internal system. ASIN is not an international
standard. You can view the ASIN of a book on the associated product page on
Amazon's website. The quickest way to find the ASIN is to look at the URL:

`https://www.amazon.com/dp/0143105434`

The ASIN usually follows directly after `dp`. For *Wuthering Heights* the ASIN
is thus `0141439556`. 

**Note:** For printed books, the ISBN-10 is usually the same as the ASIN.

* <a href="https://addons.mozilla.org/en-US/firefox/addon/asin-collector/" target="_blank" rel="noreferrer noopener">ASIN Collector</a> is a Firefox extension that can bulk-extract ASIN's for all available editions of a book.

### eBook ASIN

For eBooks the ASIN usually starts with a `B` and is listed under *Product
details*.

For example, the ASIN for *Wuthering Heights - (Penguin Classics Deluxe
Edition)* is `B0768ZM5QH`.

<Aside type="caution" title="eBook ISBN">Don't get tricked by Amazon: An
eBook product page will almost always omit the ISBN of an eBook
in favor of an ASIN. That doesn't mean that the eBook of *Wuthering Heights* is
Kindle-exclusive. You can find the associated ISBN by visiting the publisher's
website: <a
href="https://www.penguinrandomhouse.com/books/286389/wuthering-heights-by-emily-bronte/"
target="_blank" rel="noreferrer noopener">Wuthering Heights</a>' eBook ISBN is `9780525505143`.</Aside>

## Other available tools

### isbntools
* <a href="https://pypi.org/project/isbntools/" target="_blank" rel="noreferrer noopener">isbntools</a> is a python CLI application
capable of retrieving ISBN information from various sources. It can also process
multiple ISBN provided by a text-file or even other CLI programs.

Please refer to the official documentation for install instructions. Some useful commands:

```bash
# Fuzzy find an ISBN from the title (always confirm the result!)
$ isbn_from_words "mistborn final empire"
9780765311788

# Return a collection of ISBN's associated with a book
$ isbn_editions 9780765311788
9788413143194
9784150204990
9784150204952

# Get basic meta information
$ isbn_meta 9780765311788
Type:      BOOK
Title:     Mistborn - The Final Empire
Author:    Brandon Sanderson
ISBN:      9780765311788
Year:      2006
Publisher: Macmillan

# Calculate ISBN-10
$ to_isbn10 9780765311788
076531178X

# Split ISBN into its elements
$ isbn_mask 9780765311788
978-0-7653-1178-8

# Use a specific service and output-format
$ isbn_meta 9780525505143 goob json
{"type": "book",
 "title": "Wuthering Heights - (Penguin Classics Deluxe Edition)",
 "author": [{"name": "Emily Bronte"}],
 "year": "2009",
 "identifier": [{"type": "ISBN", "id": "9780525505143"}],
 "publisher": "Penguin"}
```
````

## File: src/content/docs/librarians/Standards/AuthorStandards.mdx
````
---
title: Author Standards
description: Standards for adding and editing authors in Hardcover.
category: guide
lastUpdated: 2025-09-07 16:06:00
layout: /src/layouts/librarians.astro
banner:
    content: "🚧 Mind your step, this page is a work in progress."
---

import {Badge, Aside} from "@astrojs/starlight/components";


## Author Name
The author name is the primary identifier for an author on Hardcover. It should be the name they are most commonly known by in the context of their writing, formatted in a way that is consistent with their published works.

### Authors Using Initials
Some authors use a space between initials in their name (J. K. Rowling), some do not (J.R.R. Tolkien). We should use the spacing of the author's preference (what’s used on their website or printed on their books).

When editing the URL slug for an author, do not include periods or spaces between initials (our slugs typically use lowercase letters and hyphens). For instance, J. K. Rowling’s slug would be `jk-rowling`, and J. R. R. Tolkien’s slug would be `jrr-tolkien`. Slugs are generated automatically on author generation but require manual updating when editing an existing author.

### Authors Sharing The Same Name

<Aside type="note">
This section is currently under review and will be updated in the future.
</Aside>

### Authors with Non-English Names
<Aside type="note">
In the future, Hardcover may support multiple name fields or localized names for authors. For now, stick to an English/Latin name for consistency, unless the author has absolutely no transliterated name available.
</Aside>

Hardcover’s default interface language is English. Wherever possible, we'd like to rename authors written in other alphabets (Cyrillic, Hebrew, Hanzi, Arabic, etc.) to be translated or transliterated to English (Latin alphabet). This is to ensure consistency and searchability in our primarily English database.

If an author is commonly known in English by a transliterated name, use that as the author’s name. For example, Yevgeni Grishkovetz for the Russian author Евгений Гришковец.
You may include the original-script name in the author’s profile as supplemental information. For instance, you could add the native spelling in the author’s Personal Name field (if one exists) or mention it in the biography. In the above example, you might put the Cyrillic spelling in parentheses after the English name in the bio. This way, the original name is preserved for reference.

## Photos and Biography
Author biographical information is very important to Hardcover. We'd like authors to be portrayed accurately and professionally, with the most current and verifiable information available. As such, we have strict guidelines around these pages, as well as the sources we leverage to populate them.

### General guidelines
Author bios should be concise, neutral, and factual. Focus on verifiable facts like the author’s notable works, achievements, and relevant background. Avoid subjective commentary or anything overly personal that isn’t publicly confirmed. In short, do not editorialize.

Do not include any data that has its own dedicated field, demographic or otherwise (self-identified gender, BIPOC, LGBTQ+, location, dates, etc.)

Photographs should be of the author, and not of their book covers or other images. They should be high quality and ideally a professional headshot. If the author has a preferred photo, it should be used. If not, use the most recent and high-quality image available.

### Sourcing biographical information
**Acceptable sources for author bios and photos are listed as follows, in order of authority:**

1. **Author’s official website or publications.** Many authors have an “About” page or a bio in their books. This is the most authoritative source, and often provides a bio in the author’s own words or with their approval. Author websites or an official publisher-provided author page are ideal for both biographical details and author photos.
2. **Publisher’s website.** If an author doesn’t have a personal site, the publishing house’s author page can be used. Keep in mind these might be out of date, so verify if possible.
3. **Author’s verified social media.** Sometimes authors share biographical info on profiles or posts in their own voice. This can be used, but stick to factual elements and a formal tone.
4. **Bookseller or book database bios.** Sources like Amazon Author pages or Kobo, etc., can be used only if the above sources aren’t available. These often have short blurbs. Important: If you use these, consider rewriting portions in your own words to avoid plagiarism, as they may not be author-supplied text.

**Unacceptable sources:**
1. **AI-generated content (e.g. ChatGPT).** We do not allow AI-written bios. We owe it to authors to use human-vetted information, not algorithmic guesses.
2. **Wikipedia.** Even though Wikipedia entries are convenient, we avoid copy-pasting from them.
3. **Competitor databases (Goodreads, The StoryGraph, etc.).** We aim to build Hardcover's data ourselves or from primary sources, not by copying others. Using these may also introduce licensing issues.

### Citing sources
Until we support a distinct field for bio sources, please **credit your source at the end of the bio text in parentheses**. For example, you might add: (Source: Author’s official website) at the very end of the bio. This lets users know the information’s provenance. Do not use HTML or Markdown for this note, as those won’t render properly in the app, just plain text is fine.

### Preferred file type for author photos
PNG and JPEG work the best. WebP files are not currently supported. The cover shouldn't have any transparency to it. The image is converted to a WebP file before we show it regardless of what you upload.

### Preferred file size
The larger the photo the better! If you want to upload a 15mb file, go for it. We'll resize it for optimal display around the site.

Author photos on Hardcover (as of July 27, 2025) are displayed at a maximum size of 178px by 178px. Uploading images smaller than this may result in blurriness when enlarged. For best results, we recommend uploading photos that are at least 300px wide and 300px high. Images do not need to be square.

### Image quality scores
We show three different quality scores for photos today. This is calculated using `height x width`.

0 - 32,999: <Badge text="Bad Quality" variant="danger" /> (ex 133 x 200)

33,000 - 99,999: <Badge text="Ok Quality" variant="caution" /> (ex: 200 x 300)

100,000 +: <Badge text="Good Quality" variant="success" /> (ex: 300 x 450)

## Personal Name
This field is intended only for cases where an author's full name differs from the name they publish under and is publicly known in that context (e.g., in publishing credits or legal attributions).

Do not use this field to list a birth name that an author has changed, such as after a gender transition. Avoid deadnaming, even if the information is publicly available. When in doubt, prioritize the author's privacy and self-identification over completeness. For more on this topic, see [Supporting Trans & Non-binary Authors][SupportingAuthors].

Do not use this field for pseudonyms, pen names, or stage names; on Hardcover these belong in Aliases. Enter a personal or legal name only when the author has publicly and reliably linked it to their published identity (for example, in credits, copyright or rights statements, or via self-disclosure) and when it serves a clear cataloging need such as disambiguation. If the author publishes exclusively under a pseudonym, leave this field blank unless these conditions are met. Do not infer or reveal a non-public name.

Notable Examples:
- Samuel Langhorne Clemens (Mark Twain)
- Charles Lutwidge Dodgson (Lewis Carroll)
- Mary Ann Evans (George Eliot)
- Eric Arthur Blair (George Orwell)

## Aliases
In our current implementation, we allow for a single alias per author. For authors that exist as a pseudonym, pen name, or stage name, this is the field to use to denote the primary author on Hardcover.

Examples: 
- Stephen King is the primary author, but he has written under the alias Richard Bachman.
- Isaac Asimov is the primary author, but he has written under the alias Paul French.
- Nora Roberts is the primary author, but she has written under the alias J.D. Robb.

In any of these cases, add the primary author under the "Alias of" field on the alias page.

## Demographic information
For authors, we collect the following demographic information:
- Self-identified gender
- BIPOC status
- LGBTQ+ status

These fields are optional, and we encourage librarians to only fill them out if the author has self-identified in their bio or on their website. If the author has not provided this information, please leave these fields blank.

## Location
Location information for authors is not always readily available. If the author has a location listed on their website, or in their bio, please use that information. If not, you can leave the location field blank.

For deceased authors, we recommend using the location of their birth or where they spent most of their life. If this information is not available, you can leave the location field blank.

## Dates of birth and death
If exact dates are not publicly and readily available, please use the year only in the appropriate field.

## Supporting Trans & Non-binary Authors

<Aside type="note">
This section is currently under review and will be updated in the future.
</Aside>

## Merging Authors
Sometimes an author might have multiple entries in the database (for example, due to variant spellings or a data import). When you discover duplicate author entries, they should be merged to one canonical entry. The general rule is: keep the entry with the author’s name in its most standard or canonical form (in English), and merge the other duplicate(s) into that.

For example, if you see both “J. R. R. Tolkien” and “J.R.R. Tolkien” as separate authors, we’d keep one and merge the other into it (whichever reflects our formatting guidelines best). If an author has an English name and a non-English name entry, keep the English name as primary (per our guidelines above).

For a detailed guide on merging authors, visit our [Merging Standards](../mergingstandards/#merging-authors) page.

## Author Outreach

We want authors to feel welcome on Hardcover, and Librarians are some of the best ambassadors to make that happen. Thoughtful outreach shows authors we care about how they're represented and want their profiles to shine.

We welcome librarians to contact authors on their own behalf, with the support of Hardcover. To keep things respectful and coordinated, please follow these steps:

1. **Check before contacting:** Review the [Contacted Authors List][ContactedAuthors] to be sure the author hasn't already been reached.
    - Multiple unsolicited contacts can come across as spam and reflect poorly on Hardcover. 
2. **Log the contact:** If they're not listed, add them via the [Author Outreach Form][AuthorOutreachForm].
3. **Send the outreach:** Use the [Outreach Email Template][AuthorOutreachTemplate] from your own email or an author's contact form.

By following these steps, each author gets a single, friendly introduction to Hardcover—never spam. If they respond, wonderful! If not, we've still shown care without overwhelming them.

<Aside type="tip">
Librarians discussing outreach in the Discord #librarians channel is a good way to coordinate. If you’re thinking of reaching out to a notable author, it doesn’t hurt to mention it to other librarians so everyone stays in the loop.
</Aside>

[SupportingAuthors]: #supporting-trans--non-binary-authors
[ContactedAuthors]: https://docs.google.com/spreadsheets/d/1MlaWgpBYdaLxxTwmYZxhQ0xPNqi4kZQ4J4CVPXa6Vxg/edit?gid=308756447#gid=308756447
[AuthorOutreachForm]: https://forms.gle/ewUDjfe7SV8RdaWd6
[AuthorOutreachTemplate]: https://docs.google.com/document/d/1fUmholoNHE9dR45LEREXeRUk-iwrKhlYtbzjLz9sGS8/edit?usp=sharing
````

## File: src/content/docs/librarians/Standards/BookStandards.mdx
````
---
title: Book Standards
description: Standards for adding and editing books in Hardcover.
category: guide
lastUpdated: 2025-01-07 08:00:00
layout: /src/layouts/librarians.astro
banner:
    content: "🚧 Mind your step, this page is a work in progress."
---

import {Badge} from "@astrojs/starlight/components";

## Titles
### What title should we use for the book?
We should use the official English title the book was released with whenever possible.

For example, the original title of “War and Peace” is “Война и миръ”. We should use “Война и миръ” as the title of the Russian edition, but “War and Peace” as the title of the book. This could be done from the Edit Book page where we override the edition’s title. Alternatively, we could set the “Default Physical Edition” to the English edition. That would also set the title to the English title.

If books have multiple English titles (ex: “Harry Potter and the Sorcerer's Stone” vs “Harry Potter and the Philosopher's Stone”), we should use the title localized for the USA (Sorcerers stone in this case).

In the future, we want to allow people to set their language and have it automatically use the localized version, but for now we’re aiming to use the US title as the default.

### What about franchise books, like “Brotherhood”, which is in the Star Wars universe?
In this case, the official title of the book according to the publisher is “Star Wars: Brotherhood”, and we should use that.

In other cases where there’s a series, we should leave it off unless it is part of the name (ex: Harry Potter and the Sorcerer's Stone). When left off (ex: The Fellowship of the Ring), we should make sure to set the featured series to be the primary series we know this title from (“The Lord of the Rings”).

### What if the official title also has the series in it?
To be answered!

### How should we handle books with long titles with a “:” in them? Ex: “Babel, or The Necessity of Violence: An Arcane History of the Oxford Translators' Revolution”
Set the title of this book to whatever the publisher named it. In this case, that would be “Babel, or The Necessity of Violence: An Arcane History of the Oxford Translators' Revolution”.

On the book page, we’ll break the title up by “:” and wrap it into multiple lines if it has a very long title.
<img src="/images/librarians/long-title-example.png" alt="Example of a long title on Hardcover" />

For books with a very long title, but a smaller, well-known title, we should use the shorter title as the URL slug. This allows the book to live at the URL https://hardcover.app/books/babel while maintaining a longer name. Book slugs can only be edited by the original person who added the book, Adam and Jeff right now.

### What about subtitle?
You’ll notice there’s a field for subtitle in the edit book form. We currently do not use this field for anything. We do split the title into title and subtitle when creating books. For example:

- Full title: “Wallet Activism: How to Use Every Dollar You Spend, Earn, and Save as a Force for Change”.
- Title: “Wallet Activism: How to Use Every Dollar You Spend, Earn, and Save as a Force for Change”
- Subtitle: “How to Use Every Dollar You Spend, Earn, and Save as a Force for Change”
- Slug: “wallet-activism”

## Descriptions
### Authoritative Source for Book Descriptions / Other Information
In order of preference:

1. Publisher
2. Author Official Website
3. BookBub / WorldCat
4. Bookstore (Barnes & Noble, Amazon, etc)
5. Other Book Site (Open Library, Google Books, etc)

### Promotional Content / Reviews / Author Bios / Edition Info in Descriptions
Book descriptions should be constrained to a spoiler-free introduction / summary of the book. Additional promotional information should be removed, even if it is present in the description on the authoratative source.

Examples of content to remove:
    "From the author of xxx bestselling series"
    "This book is a book -Famous Author"
    "Reprinted for the first time in genuine leather"

### Description Headlines
If available, use a headline from the publisher
If the a specific headline is not provided, there are several possible options:

1. Move the first paragraph of the description if it fits and is appropriate as a standalone
2. Copy a key sentance or phrase from the description
3. Leave it blank

## Default Editions
### Cover Edition
Generally, the cover edition should be the most recently published hardcover edition of the book with a "Good" quality cover available; however, there may be cases such as special or limited printings where another edition may be more appropriate.
````

## File: src/content/docs/librarians/Standards/ComicStandards.mdx
````
---
title: Comic Standards
description: Standards for adding and editing comics in Hardcover.
category: guide
lastUpdated: 2025-01-07 13:00:00
layout: /src/layouts/librarians.astro
banner:
    content: "🚧 Mind your step, this page is a work in progress."
---

# Comic Books
## Book Title
### Individual Issue

`{Series} #{Num}: {Title}`

    <details>
        <summary>Examples:</summary>
        The Sandman #1: Sleep of the Just

        Sage #50

        The Amazing Spider-Man #92
    </details>

### Trade Paperbacks (TPB / TP)

`{Series}, Vol. {num}: {Title}`

    <details>
        <summary>Examples:</summary>
        The Sandman, Vol. 1: Preludes & Nocturnes

        Saga, Vol. 10

        The Amazing Spider-Man, Vol. 5
    </details>

### Other Collections (Hardcover, Omnibus, Book, etc)

`{Series}: {Collection Title}`

    <details>
        <summary>Examples:</summary>
        The Sandman: Book One

        Saga: Book Three Deluxe HC

        The Amazing Spider-Man: Omnibus Vol. 1
    </details>

Issue / Volume Numbers are not added to One Shots / Standalones that do not have multiple works in the series.

Title is optional for individual issues or TPBs as not all works include them but should generally follow how the publisher lists the work. If a title is used on one book, it should be included for all books in the series.

Publication years are not added to book names unless explicitly part of the series or title from the publisher as this information in included in the series name displayed above the book.

    <details>
        <summary>Examples:</summary>
        The Amazing Spider-Man (2018) #92 -> The Amazing Spider-Man #92

        Abbott: 1979 -> Abbott: 1979
    </details>

# Comic Series

## Series Titles

### Issues

`{Series} ({Year})`

    <details>
        <summary>Examples:</summary>
        Saga

        The Amazing Spider-Man (2018-2022)

        The Amazing Spider-Man (2022-)
    </details>

### Trade Paperbacks

`{Series} ({Year}) (TPBs)`

    <details>
        <summary>Examples:</summary>
        The Sandman (TBPs)

        The Amazing Spider-Man (2012-2022) (TBP)
    </details>

### Other Collections (Hardcover, Omnibus, Book, etc)

`{Series} ({Year}) (Collection Name)`

    <details>
        <summary>Examples:</summary>
        Saga (Compendiums)
    </details>

The "primary" series (aka the series name with no additional qualifiers in the name and the shortest slug) is the most regularly released format of the series. For series that release in issues, the issues would be the primary series. If a series is released only in TPBs or Volumes, this would be the primary series.

Year is an optional field used to differentiate different comic runs under the same series name. Years for series names should use the full range of the series for completed runs or the first year and a hypen for ongoing runs.

    <details>
        <summary>Examples:</summary>
        Wonder Woman (1987-2006)

        Wonder Woman (2003-)
    </details>

Collections of works (such as TBPs for series released as issues and all other collections) should be marked as a "Compilation" with the contained issues added. The collections should be added as a "Featured" series of that format of work but not to any of the series of the books comprising the collection (E.g., The Sandman: Book Two would be added as the second item in "The Sandman (Books)" but not to "The Sandman" or "Vertigo: Winder's Edge").
````

## File: src/content/docs/librarians/Standards/Editing-FAQ.mdx
````
---
title: Editing FAQ
description: Frequently asked questions for editing books / editions.
category: guide
lastUpdated: 2025-01-07 08:00:00
layout: /src/layouts/librarians.astro
banner:
    content: "🚧 Mind your step, this page is a work in progress."
---

## General
### How do I add a book if I can't find it on Hardcover?
If you search for a book and don’t see it in the results, head over to the Add Book to Hardcover page. On there you can add a book by ISBN 10, ISBN 13 or Goodreads ID. This is the best place to start, since there’s a chance the book wasn’t showing up in search for a number of reasons (the top being that this search cache out of date, this book has recently been manually added by a user and hasn’t been approved).

If this book doesn’t have an ISBN and isn’t on Goodreads, then you can head over to the New Edition form. This will create a new Book with this as the one new edition for it. When librarians add books using this form they’ll show up for everyone right away. When guests and non-librarians add books using this form they’ll have a “user added” boolean added to that book behind the scenes that prevents it from showing up in search.

### How do I merge books?
On the book page, click the <kbd>Flag</kbd> dropdown and select <kbd>Mark as Duplicate</kbd>. This will open up a modal (or an overlay on mobile) that allows you to search for and select which book the current book is a duplicate of. Select that book and click button to mark it as a duplicate.

If your access level is greater than the impact of the merge, it’ll be merged immediately. If you try to merge a popular book into another book, the merge will be sent to an admin to double check before being run. Once it’s run you’ll receive a notification.

### When combining duplicate books/series/authors, which version should you keep?
In the case of Authors, series and characters, keep the one with the canonical English name.

For books, choose the one with the most readers using it. When another reader selects that book to read, we’ll default the “edition” that reader read to be the primary edition for this book. By selecting the book with the most readers, that means the next people who read it will also be assigned the same popular edition.

### The book cover is blurry even though the cover edition has a high resolution image
Check to make sure the file is not a webp (sometimes webp files from publishers or authors are even incorrectly marked with a .jpg extension). If this is the case you can save as in any image editor to convert to a true jpg or png before uploading to hardcover.

## Editions
### An ISBN is already in use incorrectly on another edition
Remove the ISBN from the wrong book using the <kbd>Hard Reset</kbd> button, then add it to the correct edition.

### What's the difference between 'Edition Format' and 'Reading Format' when editing a book?
On the edit edition form, we ask for both of these, but only “Reading Format” is required.
Reading format has three options: <kbd>Audiobook</kbd>, <kbd>Physical Book</kbd> and <kbd>Ebook</kbd>.

<kbd>Edition Format</kbd> is a text field that is used to elaborate on this specific edition. For example: <kbd>Hardcover</kbd>, <kbd>Mass market paperback</kbd>, <kbd>Full cast audiobook</kbd>, <kbd>Kickstarter Version</kbd>, etc.

This represents that specific edition of the book, not where you accessed it from.
It’s unlikely you’d put <kbd>Kindle Edition</kbd> here,
unless this edition was originally created for Kindle and is different from other versions.

When in doubt, and in most cases, you can leave this field blank.

## Series
### Series book count numbers low or thumbnails missing from series on author/book pages
The series book count and series previews only consider books with a published date. Check to make sure that at least one edition for all books in the series has a valid published date.

## Other
### My update didn’t work? What’s going on?
If you run into a bug, or start a thread in the bugs and questions channel with as much information as possible to help reproduce the error (link to the page you were editing, what fields you changed).
````

## File: src/content/docs/librarians/Standards/EditionStandards.mdx
````
---
title: Edition Standards
description: Standards for adding and editing editions in Hardcover.
category: guide
lastUpdated: 2025-07-27 14:00:00
layout: /src/layouts/librarians.astro
banner:
    content: "🚧 Mind your step, this page is a work in progress."
---

import {Badge} from "@astrojs/starlight/components";

## Covers
### Preferred file type for cover images
PNG and JPEG work the best. WebP files are not currently supported. The cover shouldn't have any transparency to it. The image is converted to a WebP file before we show it regardless of what you upload.

### Preferred file size
The larger the cover the better! If you want to upload a 15mb file, go for it. We'll resize it for optimal display around the site.

The covers we show on Hardcover (as of March 22, 2024) max out at 200px wide by 300px high. Uploading images smaller than this may result in blurriness when enlarged. For best results, we recommend uploading photos that are at least 300px wide by 450px high.

### What dimensions qualify for red, yellow and green?
We show three different quality scores for covers today. This is calculated using `height x width`.

0 - 32,999: <Badge text="Bad Quality" variant="danger" /> (ex 133 x 200)

33,000 - 99,999: <Badge text="Ok Quality" variant="caution" /> (ex: 200 x 300)

100,000 +: <Badge text="Good Quality" variant="success" /> (ex: 300 x 450)

We'd like to start showing larger covers on the book page, which will require more covers in the Great Quality range.

## Contributors
### Order of Listing Edition Contributors
Add the primary authors in the same order as they appear on the cover of the book. Additional contributors (editors, illustrators, etc) can be added in any order.

### Anthologies with Multiple Authors
For works containing numerous authors, such as anthologies of short stories, all contributing authors should be listed under the author role.

    <details>
        <summary>Examples:</summary>
        Unbound, published by Grim Oak Press shows the Author as "Multiple" and lists the Authors and their contributed works in the description.

        In this case, all 23 of the contributing authors should be listed as an Author on the edition.
    </details>

## Publishing Information
### Publisher Name
List the name of the company that published this edition.

Authors self-publishing under their own name should be entered as "Independently Published". Small companies, including LLCs established by the author that only publish that author's works, are still have the company name listed.

Do not include commas or periods around business entity acronyms.

    <details>
        <summary>Examples:</summary>
        Julie Carobini -> Indepenently Published

        Julie Carobini, LLC -> Julie Carobini LLC

        Julie Carobini Inc. -> Julie Carobini Inc
    </details>

### Published Date
List the date of publication for the edition provided by the publisher. It is important that at least one edition of a book have a valid publishing date for proper book display in series or other places. Hardcover will automatically select the earliest publication date for display on the book.

If a specific date of publishing does not exist or cannot be found, list the date as Jan 1 of that year. If a month but not day is available, list it as the first day of that month: 1/1/year
````

## File: src/content/docs/librarians/Standards/MergingStandards.mdx
````
---
title: Merge / Split Standards
description: Standards for merging or splitting various objects on Hardcover.
category: guide
lastUpdated: 2025-08-22 14:00:00
layout: /src/layouts/librarians.astro
banner:
    content: "🚧 Mind your step, this page is a work in progress."
---

import { URLS } from "@/Consts";
import { Image } from 'astro:assets';
import {Aside} from "@astrojs/starlight/components";
import merge_book_flag from 'src/content/images/merge_book_flag.png'; 
import merge_book_select from 'src/content/images/merge_book_select.png';
import merge_ed_flag from 'src/content/images/merge_ed_flag.png'; 
import merge_ed_select from 'src/content/images/merge_ed_select.png';
import merge_ed_change from 'src/content/images/merge_ed_change.png';
import split_ed_list from 'src/content/images/split_ed_list.png';
import split_ed_change from 'src/content/images/split_ed_change.png';
import merge_author_flag from 'src/content/images/merge_author_flag.png';
import merge_author_select from 'src/content/images/merge_author_select.png';
import merge_series_flag from 'src/content/images/merge_series_flag.png';
import merge_series_select from 'src/content/images/merge_series_select.png';

## Merging Books
<Image src={merge_book_flag} alt="Flag the duplicate book" />
On the page for the book you want to merge (i.e., the duplicate), click the edit button and select the "Flag as Duplicate" option from the dropdown.

<Image src={merge_book_select} alt="Select which book to keep" />
You will be presented with a search box to select the canonical book listing (i.e., the one you want to keep). Start typing the name of the book you want to merge into and select it from the dropdown list.

Once selected, the book will be highlighted in green and you will be presented with the option of which book to keep. At this time, we recommend selecting the book with the nicer slug. `le-dame-di-grace-adieu-e-altre-storie` being less desirable than `the-ladies-of-grace-adieu-and-other-stories`.

After clicking the "Keep this one" button, your merge will be submitted. In some cases, where the book's impact score is high, this will require approval from a Senior Librarian on the Hardcover team before it is finalized. In the event that it's immediately approved, the page will redirect to the new canonical book page.

## Merging Editions
<Aside type="caution">
This feature behaves a little differently from other merges. Please read the following carefully and, if there's any doubt, ask in the <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a> channel before proceeding.
</Aside>

There will be times when two editions of a book are actually the same. Typically these are editions with no IDs (ISBN, ASIN, etc.) or otherwise missing metadata that exists on another existing edition. In these cases, we can clean up by merging these editions together.

**When not to merge editions:**
- Different IDs (e.g., ISBNs, ASINs)
- Different formats (e.g., Audiobook vs. eBook)
- Different languages (e.g., English vs. Spanish)
- Different publishers (e.g., Penguin vs. HarperCollins)

<Image src={merge_ed_flag} alt="Flag the duplicate edition" />
From the edition list of the book that has a duplicate edition, select the duplicate and click the "Flag as Duplicate" option from the edit dropdown.

<Image src={merge_ed_select} alt="Select the canonical edition" />
In the modal that appears, select the canonical edition (i.e., the one you want to keep) from the dropdown list. Its selection will be confirmed by a filled-in radio button to the left of the edition details.

<Image src={merge_ed_change} alt="Submit the edition merge" />
It's important that the edition to be merged is the one you started from. The edition you want to keep is the one you are selecting from the list in the modal.

Once you've selected the canonical edition, scroll back up to the top of the list, taking care not to change the selection as you go. Once you're sure your selection is correct, click the red button.


## Splitting Editions
<Aside type="caution">
This feature is currently granted on an individual basis to experienced librarians. If you do not have access to this feature, you can either report offending edition using the "Report a problem" button or post in the <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a> channel for assistance.
</Aside>

There will be times when a title has been added as an edition to the wrong book. To fix this, we can split the edition out, either into an existing book or a new one.

<Aside type="note">
It's important to check the mappings on editions before splitting them. If the edition has mappings that belong to another book, such as the one it's been mistakenly assigned to, these will need to be removed before the split. The consequence is moving reads and reviews to the incorrect book, even if the moved edition's metadata is correct.
</Aside>

<Image src={split_ed_list} alt="Edit the edition that doesn't belong" />
From the edition list of the book that has the incorrect edition, select the edition you want to split out and click the edit button.

<Image src={split_ed_change} alt="Edit the edition that doesn't belong" />
In the book box on the edition edit page, click the "Change?" button. This will open a search box where you can search for the correct book to move the edition to. If the correct book does not exist, you can create a new one by clicking the "No book exists. Create a new book" option at the top of the dropdown list.

This will move the edition and all of its associated data (like covers, ISBNs, readers, etc.) to its new destination.

## Merging Authors
<Image src={merge_author_flag} alt="Flag the duplicate author" />
On the page for the author you want to merge (i.e., the duplicate), click the edit button and select the "Flag as Duplicate" option from the dropdown.

<Image src={merge_author_select} alt="Select which author to keep" />
You will be presented with a search box to select the canonical author listing (i.e., the one you want to keep). Start typing the name of the author you want to merge into and select them from the dropdown list.

Once selected, the author will be highlighted in green and you will be presented with the option of which author to keep. At this time, we recommend selecting the author with the nicer slug. `clarke-susanna-453d6bb8-3374-4d57-9d78-0135780dd030` being less desirable than `susanna-clarke`.

After clicking the "Keep this one" button, your merge will be submitted. In many cases, where the author's impact score is high, this will require approval from a Senior Librarian on the Hardcover team before it is finalized. In the event that it's immediately approved, the page will redirect to the new canonical author page.

## Merging Series
<Image src={merge_series_flag} alt="Flag the duplicate series" />
On the page for the series you want to merge (i.e., the duplicate), click the edit button and select the "Flag as Duplicate" option from the dropdown.

<Image src={merge_series_select} alt="Select which series to keep" />
You will be presented with a search box to select the canonical series (i.e., the one you want to keep). Start typing the name of the series you want to merge into and select it from the dropdown list.

Once selected, the series will be highlighted in green and you will be presented with the option of which one to keep. At this time, we recommend selecting the series with the nicer slug. For *Strange & Norrell*, `strange-and-norrell` would be preferable to `strange-norrell`.

After clicking the "Keep this one" button, your merge will be submitted. In many cases, where the series' impact score is high, this will require approval from a Senior Librarian on the Hardcover team before it is finalized. In the event that it's immediately approved, the page will redirect to the new canonical series page.

## Merging Publishers
<Aside type="note">
Due to some known bugs, this section is currently under review and will be updated in the future. Publisher merges are currently being held in the Senior Librarian review queue until this is resolved.
</Aside>
````

## File: src/content/docs/librarians/Standards/SeriesStandards.mdx
````
---
title: Series Standards
description: Standards for adding and editing series in Hardcover.
category: guide
lastUpdated: 2025-02-08 09:57:47
layout: /src/layouts/librarians.astro
banner:
    content: "🚧 Mind your step, this page is a work in progress."
---

## Duplicate Series Names
For multiple series with the same name, adjust the additional series as follows:
  - Append `(Author Name)` to the series name 
  - Append `-AuthorName` to the slug

When a series has been adapted into a different format (e.g., a manga that was novelized), we create a separate series for the adaptation:
  - The source format retains the series name (e.g., `The Summer Hikaru Died`)
  - For the adaptation, append `(Format)` to the series name (e.g., `The Summer Hikaru Died (Light Novel)`
  - For the adaptation, append `-format` to the slug (e.g., `the-summer-hikaru-died-lightnovel`)


## Publisher Collections (E.g., Penguin Little Black Classics)
For publisher or other collections where only a specific edition of a book is part of the series, a Hardcover series should not be created. The book may be instead added to a list.
````

## File: src/content/docs/librarians/FAQ.mdx
````
---
title: Librarian FAQ
description: Frequently asked questions for librarians.
category: guide
lastUpdated: 2025-09-18 15:05:00
layout: /src/layouts/librarians.astro
---

import { URLS } from "@/Consts";

## Known issues
*Before checking out the FAQ, please be aware of the following known issues:*

- There are known issues around the propagation of deduplicated authors to editions. This is being actively worked on and should be resolved in the near future.
- It is known that random book covers have been assigned to author pages throughout the site. We're aware of this and are working on a fix.
- If a book is a member of a series but isn't appearing on the series page, please check if the book has a value other than a number in the `Place in series (text)` field. If it does, please remove anything that isn't a number (Vol., tome, short story titles) and save the book. The book should then appear on the series page.
- It is known that publisher merges don't stick after a book with a merged publisher is edited.

## Frequently Asked Questions

*While the Librarian docs are fairly comprehensive, there are a few questions that come up often enough that it makes sense to address them here.*

### What's to stop a librarian from messing up a book/author/etc?
For books / editions / with a high `impact_score`, meaning anything with five or more reads, there is a check in place that requires a member of the Hardcover Senior Librarian team’s approval before the change takes place.

### How do I report bugs?
Hardcover is under active development and sometimes things break as we add features. We want to fix issues as soon as possible, so thank you for your reports and patience! 😅

The best way to report a bug is via <a href={URLS.BUGS_DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>. Head to the #bugs channel and do a quick search to check whether the current issue has already been posted. If not, provide details such as: links to the page you were editing, what actions were taken, and what happened as a result (especially if there was an error message or weird behavior).

Screenshots can help if applicable (including console output if you’re comfortable with your browser’s dev tools). By reporting in Discord, other <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a> or developers can confirm if it’s a known bug or offer a workaround while a fix is being worked on.

We truly appreciate bug reports, they help us improve the site for everyone!
````

## File: src/content/docs/librarians/Getting-Started.mdx
````
---
title: Getting Started as a librarian
description: Get started contributing to Hardcover as a librarian.
category: guide
lastUpdated: 2025-09-18 15:05:00
layout: /src/layouts/librarians.astro
---

import { URLS } from "@/Consts";
import {Aside} from "@astrojs/starlight/components";

## The Librarian role

Librarians are trusted members of the Hardcover community who have been granted additional editing privileges. They are volunteer editors tasked with the responsibility of maintaining data quality across the platform.

## Eligibility

Anyone with a passion for books and data can apply to become a librarian. There are no strict prerequisites like number of books read or technical skills - we welcome volunteer contributors who are detail-oriented and want to help maintain our book database. Every new librarian application is reviewed by the Hardcover team for approval. We look for users who have shown genuine interest in the platform and will uphold our data standards. If you're enthusiastic about keeping book information accurate and complete, you're eligible to apply!

## Application Process

<Aside type="caution">
We are currently reviewing our Librarian onboarding process and new librarian applications are currently on hold. Please check back in a few months or reach out on <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a> if you have questions.
</Aside>

Simply fill out the <a href={URLS.LIBRARIAN_APPLICATION} target="_blank" rel="noreferrer noopener">librarian application form</a> on our website. After you submit your application, you will be required to join our <a href={URLS.DISCORD} target="_blank" rel="noreferrer noopener">Discord</a>. Once there, the team will review your application. There’s no set timeline for approval, but feel free to ping `@team-librarians` if you have been waiting for over a month.

If approved, you will receive an email with further instructions on how to get started as a librarian. You'll also be asked to <a href={URLS.LINK_ROLES} target="_blank" rel="noreferrer noopener">link your role</a> to grant you access to our <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a> collaboration channel, where you can ask questions, get clarification on policies, and receive help from other librarians and the Hardcover team.

## Responsibilities

Librarians are volunteer editors, they can contribute as much or as little as time allows. The role and its enhanced privileges come with the responsibility of maintaining data quality. They are expected to follow the standards and operate within guidelines outlined on this site. They use good judgment when taking action around the platform and ask questions when unsure.

We expect librarians to act in good faith and aim for accuracy and consistency in the database. The librarian role is not a status symbol or a way to gain influence - it is a shared responsibility to help keep Hardcover's data accurate and reliable for all users.

The community of librarians is collaborative and supportive. The <a href={URLS.LIBRARIAN_DISCORD} target="_blank" rel="noreferrer noopener">#librarians</a> channel is a great place to discuss tricky edits, ask for help, and share knowledge. We operate with a collaborative spirit - no one is expected to know everything, and we all learn from each other. Contributions of any size are welcome and appreciated.

## Access & privileges

As a librarian, you can edit most [book](./standards/bookstandards/), [edition](./standards/editionstandards/), [series](./standards/seriesstandards/) and [author](./standards/authorstandards/) fields in the database. We plan to expand librarian abilities to other data types as well (characters, publishers, etc.)

Other tools available include options to flag duplicates (for [merging](./standards/mergingstandards/)) or split incorrectly merged editions. High-impact actions (like merging popular books or deleting entries) may require additional approval from a Senior Librarian on the Hardcover team.

## Combining Supporter roles

If you are already a librarian, you can also <a href={URLS.MEMBERSHIP} target="_blank" rel="noreferrer noopener">become a supporter</a>. Supporters inherit all of the editing powers enjoyed as a Librarian plus a profile badge, early-access features, and other perks yet to come while directly funding Hardcover's ongoing development.

Many volunteers choose to be both: your librarian privileges stay permanent, and the supporter benefits stay active for as long as your paid plan is. If you are already a librarian and cancel your supporter membership, only the extra perks tied to the subscription disappear. Your librarian status (and its editing privileges) remain unchanged.
````

## File: src/content/docs/404.mdx
````
---
title: '404'
template: splash
editUrl: false
hero:
    title: '404'
    tagline: The requested page was not found. Check the URL or <br /> try using the search bar above or one of the options below.
---

import { LinkCard } from '@astrojs/starlight/components';
import { URLS } from '@/Consts';


<LinkCard title="Documentation Home"
          description="Go back to the documentation home page"
          href="/"
/>

<LinkCard title="Hardcover App"
          description="Go to the Hardcover app"
          href={URLS.APP}
          target="_blank"
/>
````

## File: src/content/docs/index.mdx
````
---
title: Welcome to the Hardcover docs!
description: Get started contributing to Hardcover
lastUpdated: 2025-05-02 23:50:00
template: splash
hero:
    title: Welcome to the Hardcover docs!
    tagline: Get started contributing to Hardcover
    image:
        file: /src/assets/hardcover-hero.png
        alt: Hardcover logo
    actions:
        - text: API Docs
          link: ./api/getting-started
          variant: primary
        - text: Contributing Guides
          link: ./contributing
          variant: primary
        - text: Librarian Guides
          link: ./librarians/faq
          variant: primary
---

import { LinkCard } from '@astrojs/starlight/components';
import { URLS } from '@/Consts';

<LinkCard title="Return to Hardcover App" href={URLS.APP} target="_blank" rel="noreferrer noopener" />
````

## File: src/content/docs/ui.json
````json
{
  "lang": {
    "label": "English",
    "code": "en"
  },
  "pages": {
    "api": {
      "disclaimerBanner": {
        "title": "Disclaimer",
        "text": "This API is currently in development and may change or break at any time with out notice. If you have any questions or need help, please ask in the <a>#api</a> Discord channel."
      }
    },
    "librarians": {
      "standardsBanner": {
        "title": "Note",
        "text": "The rules and guidelines included in the standards sections of this documentation are intended to provide a general framework to guide new librarians, provide examples about how to handle common editing scenarios, and present consistency across the site. That said, no two books are the same, and so it is impossible for any single standard to be perfectly applicable in all situations. If you believe a particular work does not fit into these standards or have suggestions for improvement, please let us know in the <a>#librarians</a> Discord channel."
      }
    }
  },
  "sidebar": {
    "api": {
      "title": "API Docs",
      "gettingStarted": "Getting Started",
      "guides": "Guides",
      "schemas": "Schemas"
    },
    "contributing": {
      "title": "Contributing Guides"
    },
    "librarians": {
      "title": "Librarian Guides",
      "editing": "Editing FAQ",
      "faq": "Librarian FAQ",
      "gettingStarted": "Getting Started as a Librarian",
      "resources": "Resources",
      "standards": "Standards"
    }
  },
  "site": {
    "title": "Hardcover"
  },
  "ui": {
    "lastUpdated": "Last Updated",
    "graphQLExplorer": {
      "query": "Query",
      "example": "Example query",
      "viewQuery": "View query",
      "results": "Results",
      "tryIt": "Try it yourself",
      "authToken": "Authorization Token",
      "authTokenDescription": "This token will be used to authenticate your requests. You can find it in your account settings.",
      "run": "Run query",
      "runDescription": "Run the query displayed below",
      "views": {
        "default": "Default view",
        "chart": "Chart view",
        "json": "JSON view",
        "table": "Table view"
      },
      "statusMessages": {
        "warning": "Warning!",
        "disclaimer": "This will run against your account. You are responsible for the content of any queries ran on your account.",
        "loading": "Loading...",
        "error": "Error",
        "errorRunning": "Error running query",
        "connectionError": "Error connecting to server",
        "emptyQuery": "No query provided",
        "mutationQueryNotAllowed": "Mutation queries are not currently allowed in this explorer",
        "invalidQuery": "Invalid query",
        "emptyToken": "No auth token provided",
        "invalidToken": "Invalid or expired auth token",
        "success": "Success!",
        "noResults": "No results found",
        "viewUnavailable": "This view is not available for this query's results."
      }
    }
  }
}
````

## File: src/content/config.ts
````typescript
import { defineCollection } from 'astro:content';
import { docsLoader} from "@astrojs/starlight/loaders";
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema()
	}),
};
````

## File: src/layouts/documentation.astro
````
---
import {Badge} from '@astrojs/starlight/components';

import {uCFirst, useTranslation} from "@/lib/utils";
import type { FrontmatterConfig } from '@/types';
import { Components } from "@/components";

const {
    author,
    banner,
    category,
    description,
    draft,
    editUrl,
    head,
    hero,
    lastUpdated,
    next,
    prev,
    sidebar,
    slug,
    template,
    title,
} = Astro.props.frontmatter as FrontmatterConfig;

const locale = Astro.currentLocale;


---

<div class="flex flex-auto flex-row justify-between mb-4">
    <p class="text-sm inline-block self-start">
        {lastUpdated && (
                <>
                    {useTranslation('ui.lastUpdated', locale)} &nbsp; {new Date(lastUpdated).toLocaleDateString(locale, {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                })}
                </>
        )}
    </p>
    {category && (
            <Badge text={uCFirst(category)} variant="note" class="w-fit"/>
    )}
</div>

<Components.banners.api locale={locale} client:only="react"/>

<slot/>
````

## File: src/layouts/librarians.astro
````
---
import {Badge} from '@astrojs/starlight/components';

import {uCFirst, useTranslation} from "@/lib/utils";
import type {FrontmatterConfig} from '@/types';
import { Components } from '@/components';

const {
    author,
    banner,
    category,
    description,
    draft,
    editUrl,
    head,
    hero,
    lastUpdated,
    next,
    prev,
    sidebar,
    slug,
    template,
    title,
} = Astro.props.frontmatter as FrontmatterConfig;

const locale = Astro.currentLocale;
---

<div class="flex flex-auto flex-row justify-between mb-4">
    <p class="text-sm inline-block self-start">
        {lastUpdated && (
                <>
                    {useTranslation('ui.lastUpdated', locale)}
                    &nbsp; {new Date(lastUpdated).toLocaleDateString(locale, {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                })}
                </>
        )}
    </p>
    {category && (
            <Badge text={uCFirst(category)} variant="note" class="w-fit"/>
    )}
</div>

<Components.banners.librarian locale={locale} client:only="react"/>

<slot/>
````

## File: src/lib/translations.ts
````typescript
/**
 * This file is responsible for loading the translations for the UI components.
 * Currently only the UI components are translated here.
 * Page translations are handled in the mdx files.
 * Example:
 * `src/content/docs/it/ui.json` -- Italian translations for the UI components
 * `src/content/docs/it/librarians/FAQ.mdx` -- Italian translations for the FAQ page
 *
 * Translations are provided by the community and are not guaranteed to be complete.
 *
 * In the future this will likely be replaced with `react-intl` or `react-i18next`
  */

import * as IT from '../content/docs/it/ui.json';
import * as EN from '../content/docs/ui.json';

const locales = {
    en: EN,
    it: IT,
}

const defaultLocale = "en";

/**
 * Try to get the specified locale from the locales object. If it doesn't exist, return the default locale.
 * @param locale
 * @returns The locale object
 * @example
 * ```ts
 * import { getLocale } from "@/lib/utils"
 * const locale = getLocale("it");
 * // locale would be the Italian translations object
 * ```
 */
const getLocale = (locale: string) => {
    // @ts-ignore
    return locales[locale] || locales[defaultLocale];
}

/**
 * Split the translation key into an array of strings.
 * @param key
 * @returns The split translation key
 * @example
 * ```ts
 * import { splitTranslationKey } from "@/lib/utils"
 * const key = "ui.greeting";
 * const splitKey = splitTranslationKey(key);
 * // splitKey would be ["ui", "greeting"]
 * ```
 */
const splitTranslationKey = (key: string) => {
    return key.split('.');
}

/**
 * Utility function to get the translation for a given key and locale
 *
 * In the future this will likely be replaced with `react-intl` or `react-i18next`
 * @param key
 * @param locale
 * @returns The translation for the given key and locale as a string
 * @example
 * ```ts
 * import { useTranslation } from "@/lib/utils"
 * const translation = useTranslation("ui.greeting", "it");
 * // translation would be "Ciao"
 * ```
 */
export const getTranslationNode = (key: string, locale: string) => {
    const data = getLocale(locale);
    const splitKey = splitTranslationKey(key);

    let node = data;
    for (const k of splitKey) {
        node = node && Object.keys(node).includes(k) ? node[k] : null;
    }

    if (node) {
        return node;
    }

    // If the node doesn't exist for the specified locale, return the en translation
    let enNode = getLocale('en');

    for (const k of splitKey) {
        enNode = enNode && Object.keys(enNode).includes(k) ? enNode[k] : null;
    }

    if (enNode) {
        return enNode;
    }

    return null;
}
````

## File: src/lib/utils.test.ts
````typescript
import {describe, expect, test} from 'vitest'
import {cn, uCFirst} from "./utils.ts";

describe('uCFirst', () => {
    test('with mode "first" / default', () => {
        expect(uCFirst('hello')).toBe('Hello');
        expect(uCFirst('world')).toBe('World');
        expect(uCFirst('')).toBe('');
        expect(uCFirst('hello world!')).toBe('Hello world!');

        expect(uCFirst('hello world. how are you?', 'first')).toBe('Hello world. how are you?');
        expect(uCFirst('hello world!', 'first')).toBe('Hello world!');
    });

    test('with mode "words"', () => {
        expect(uCFirst('hello world', 'words')).toBe('Hello World');
        expect(uCFirst('hello world!', 'words')).toBe('Hello World!');
        expect(uCFirst('hello world. how are you?', 'words')).toBe('Hello World. How Are You?');
    });

    test('with mode "sentences"', () => {
        expect(uCFirst('hello world', 'sentences')).toBe('Hello world');
        expect(uCFirst('hello world!', 'sentences')).toBe('Hello world!');
        expect(uCFirst('hello world. how are you?', 'sentences')).toBe('Hello world. How are you?');
    });
});

describe('cn', () => {
    test('cn with multiple strings', () => {
        expect(cn('text-center', 'text-blue-500')).toBe('text-center text-blue-500');
        expect(cn('text-center', 'text-blue-500', 'text-lg')).toBe('text-center text-blue-500 text-lg');
    });

    test('cn with empty string', () => {
        expect(cn('text-center', '')).toBe('text-center');
        expect(cn('', 'text-blue-500')).toBe('text-blue-500');
        expect(cn('', '')).toBe('');
    });

    test('cn with undefined', () => {
        expect(cn('text-center', undefined)).toBe('text-center');
        expect(cn(undefined, 'text-blue-500')).toBe('text-blue-500');
        expect(cn(undefined, undefined)).toBe('');
    });

    test('cn with null', () => {
        expect(cn('text-center', null)).toBe('text-center');
        expect(cn(null, 'text-blue-500')).toBe('text-blue-500');
        expect(cn(null, null)).toBe('');
    });

    test('cn with false', () => {
        expect(cn('text-center', false)).toBe('text-center');
        expect(cn(false, 'text-blue-500')).toBe('text-blue-500');
        expect(cn(false, false)).toBe('');
    });
});
````

## File: src/lib/utils.ts
````typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

import { defaultPreferences } from "../Consts"
import { getTranslationNode } from "./translations.ts";

/**
 * Utility function to merge class names
 * @param inputs - Class names to merge
 * @returns Merged class names as a string
 * @example
 * ```ts
 * import { cn } from "@/lib/utils"
 * const className = cn("bg-red-500", "text-white", { "font-bold": true })
 * // className will be "bg-red-500 text-white font-bold"
 * ```
 */

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}


/**
 * Capitalizes the first letter of a string, each word, or the first letter of each sentence.
 * @param str
 * @param mode - The mode to use for capitalization.
 * Can be 'words', 'sentences', or 'first'.
 * Default is 'first'.
 *
 * @returns The capitalized string
 * @example
 * ```ts
 * import { uCFirst } from "@/lib/utils"
 * const capitalized = uCFirst("hello world")
 * // capitalized will be "Hello world"
 *
 * const capitalizedWords = uCFirst("hello world", "words")
 * // capitalizedWords will be "Hello World"
 *
 * const capitalizedSentences = uCFirst("hello world. how are you?", "sentences")
 * // capitalizedSentences will be "Hello world. How are you?"
 * ```
 */
export const uCFirst = (str: string, mode: 'words' | 'sentences' | 'first' = 'first') => {
    switch (mode) {
        case 'words':
            return str.replace(/\b\w/g, char => char.toUpperCase());
        case 'sentences':
            return str.replace(/(^\s*\w|[.!?]\s*\w)/g, char => char.toUpperCase());
        case 'first':
        default:
            return str.charAt(0).toUpperCase() + str.slice(1);
    }
};


/**
 * Utility function to get the translation for a given key and locale
 *
 * In the future this will likely be replaced with `react-intl` or `react-i18next`
 * @param key
 * @param locale
 * @returns The translation for the given key and locale as a string
 * @example
 * ```ts
 * import { useTranslation } from "@/lib/utils"
 * const translation = useTranslation("ui.greeting", "it");
 * // translation would be "Ciao"
 * ```
 */
export const useTranslation = (key: string, locale: string = 'en') => {
    return getTranslationNode(key, locale);
};

/**
 * Utility function to get the translation for a given key and locale with tokens.
 *
 * See `/contributing/using-translations` for more information on how to use tokens.
 *
 * In the future this will likely be replaced with `react-intl` or `react-i18next`
 *
 * @param key
 * @param locale
 * @param tokens
 * @returns The translation for the given key and locale with tokens replaced
 * @example
 * ```ts
 * import { useTokenTranslation } from "@/lib/utils"
 * const name = "John";
 * const translation = useTokenTranslation("ui.token_greeting", "it", { "name": () => name });
 * // translation would be "Ciao John"
 * ```
 */
export const useTokenTranslation = (key: string, locale: string = 'en', tokens: object) => {
    let node = getTranslationNode(key, locale);

    if (typeof node === 'string') {
        Object.entries(tokens).forEach(([key, value]) => {
            const tokenRegex = new RegExp("\<" + key + "\>(.*?)\<\/" + key + "\>", 'g');
            const matches = node.match(tokenRegex);

            if (matches) {
                matches.forEach((match: string) => {
                    const tokenValue = match.replace(tokenRegex, '$1');
                    let tokenReplacement = value(tokenValue);
                    tokenReplacement = tokenReplacement.replace('{chunks}', tokenValue);

                    node = node.replace(match, tokenReplacement);
                });
            }
        });

        return node;
    }
}

/**
 * Get the user preference from local storage<br>
 * This is used to store the user's theme, component settings, etc.<br>
 * Local storage is only available in the React components
 * @param key
 * @returns The user preference for the given key as a string
 */
export const getPreference = (key: string) => {
    if (typeof window !== 'undefined') {
        const preference = localStorage.getItem(key);

        if (preference) {
            return JSON.parse(preference);
        }

        return getDefaultPreference(key);
    }

    return getDefaultPreference(key);
}

/**
 * Get the default value for a given key<br>
 * This is used when the user preference is not set
 * @param key
 */
export const getDefaultPreference = (key: string) => {
    if (key in defaultPreferences) {
        // @ts-ignore TS7053 implicitly has an 'any' type
        return defaultPreferences[key];
    }

    return null;
}


/**
 * Set the user preference in local storage<br>
 * Local storage is only available in the React components
 * @param key
 * @param value
 */
export const setPreference = (key: string, value: any) => {
    if (typeof window !== 'undefined') {
        localStorage.setItem
            (key, JSON.stringify(value));
    }
}

/**
 * Remove the user preference from local storage<br>
 * Local storage is only available in the React components
 * @param key
 */
export const removePreference = (key: string) => {
    if (typeof window !== 'undefined') {
        localStorage.removeItem(key);
    }
}
````

## File: src/Consts.ts
````typescript
export const URLS = {
    APP: 'https://hardcover.app',
    API: 'https://api.hardcover.app',
    API_ACCOUNT_URL: 'https://hardcover.app/account/api',
    DOCS: 'https://docs.hardcover.app',

    GRAPHQL_URL: 'https://api.hardcover.app/v1/graphql',

    GITHUB: 'https://github.com/hardcoverapp/hardcover-docs/',
    GITHUB_EDIT: 'https://github.com/hardcoverapp/hardcover-docs/edit/main/',
    GITHUB_DEV: 'https://github.dev/hardcoverapp/hardcover-docs/blob/main/',

    ISSUES: 'https://github.com/hardcoverapp/hardcover-docs/issues',
    CREATE_ISSUE: 'https://github.com/hardcoverapp/hardcover-docs/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=',
    SUGGEST_FEATURE: 'https://github.com/hardcoverapp/hardcover-docs/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=',

    DISCORD: 'https://discord.gg/edGpYN8ym8',
    API_DISCORD: 'https://discord.com/channels/835558721115389962/1278040045324075050',
    BUGS_DISCORD: 'https://discord.com/channels/835558721115389962/1105920773257953310',
    LIBRARIAN_DISCORD: 'https://discord.com/channels/835558721115389962/1105918193022812282',
    
    LIBRARIAN_APPLICATION: 'https://hardcover.app/librarians/apply',
    MEMBERSHIP: 'https://hardcover.app/account/membership',
    LINK_ROLES: 'https://hardcover.app/pages/how-to-link-hardcover-roles-with-discord',

    APP_STORE: 'https://apps.apple.com/us/app/hardcover-app/id1663379893',
    PLAY_STORE: 'https://play.google.com/store/apps/details?id=hardcover.app',

    INSTAGRAM: 'https://instagram.com/hardcover.app',
    MASTODON: 'https://mastodon.hardcover.app/@hardcover',
};

export const defaultPreferences: {
    theme: 'auto' | 'dark' | 'light';
    editMode: 'basic' | 'developer';
    graphQLResults: 'table' | 'json';
} = {
    theme: 'auto',
    editMode: 'basic',
    graphQLResults: 'table',
}
````

## File: src/env.d.ts
````typescript
/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />
````

## File: src/tailwind.css
````css
@tailwind base;
@tailwind components;
@tailwind utilities;

/*
Add additional Tailwind styles to this file, for example with @layer:
https://tailwindcss.com/docs/adding-custom-styles#using-css-and-layer
*/

@layer base {
    :root {
        --background: 0 0% 100%;
        --foreground: 222.2 84% 4.9%;
        --card: 0 0% 100%;
        --card-foreground: 222.2 84% 4.9%;
        --popover: 0 0% 100%;
        --popover-foreground: 222.2 84% 4.9%;
        --primary: 221.2 83.2% 53.3%;
        --primary-foreground: 210 40% 98%;
        --secondary: 210 40% 96.1%;
        --secondary-foreground: 222.2 47.4% 11.2%;
        --muted: 210 40% 96.1%;
        --muted-foreground: 215.4 16.3% 46.9%;
        --accent: 210 40% 96.1%;
        --accent-foreground: 222.2 47.4% 11.2%;
        --destructive: 0 84.2% 60.2%;
        --destructive-foreground: 210 40% 98%;
        --border: 214.3 31.8% 91.4%;
        --input: 214.3 31.8% 91.4%;
        --ring: 221.2 83.2% 53.3%;
        --radius: 0.5rem;
        --chart-1: 12 76% 61%;
        --chart-2: 173 58% 39%;
        --chart-3: 197 37% 24%;
        --chart-4: 43 74% 66%;
        --chart-5: 27 87% 67%;
    }

    .dark {
        --background: 222.2 84% 4.9%;
        --foreground: 210 40% 98%;
        --card: 222.2 84% 4.9%;
        --card-foreground: 210 40% 98%;
        --popover: 222.2 84% 4.9%;
        --popover-foreground: 210 40% 98%;
        --primary: 217.2 91.2% 59.8%;
        --primary-foreground: 222.2 47.4% 11.2%;
        --secondary: 217.2 32.6% 17.5%;
        --secondary-foreground: 210 40% 98%;
        --muted: 217.2 32.6% 17.5%;
        --muted-foreground: 215 20.2% 65.1%;
        --accent: 217.2 32.6% 17.5%;
        --accent-foreground: 210 40% 98%;
        --destructive: 0 62.8% 30.6%;
        --destructive-foreground: 210 40% 98%;
        --border: 217.2 32.6% 17.5%;
        --input: 217.2 32.6% 17.5%;
        --ring: 224.3 76.3% 48%;
        --chart-1: 220 70% 50%;
        --chart-2: 160 60% 45%;
        --chart-3: 30 80% 55%;
        --chart-4: 280 65% 60%;
        --chart-5: 340 75% 55%;
    }
}

kbd {
    background-color: hsl(var(--card));
    color: hsl(var(--card-foreground));
    border-radius: 4px;
    border: 1px solid var(--border);
    padding: 0.1rem 0.3rem;
    font-size: 0.9em;
    font-family: Monospaced, monospace;
}
````

## File: src/types.ts
````typescript
// Mainly copied from the Starlight schemas, with minor changes, and placed here for simplicity.

export interface BadgeConfig {
    text: string;
    variant?: 'note' | 'tip' | 'caution' | 'danger' | 'success' | 'default';
    class?: string;
}

export interface BannerConfig {
    content: string;
}

export interface HeadConfig {
    tag: string;
    attrs?: Record<string, string | boolean | undefined>;
    content?: string;
}

export interface HeroConfig {
    title?: string;
    tagline?: string;
    image?:
        | {
        // Relative path to an image in your repository.
        file: string;
        // Alt text to make the image accessible to assistive technology
        alt?: string;
    }
        | {
        // Relative path to an image in your repository to be used for dark mode.
        dark: string;
        // Relative path to an image in your repository to be used for light mode.
        light: string;
        // Alt text to make the image accessible to assistive technology
        alt?: string;
    }
        | {
        // Raw HTML to use in the image slot.
        // Could be a custom `<img>` tag or inline `<svg>`.
        html: string;
    };
    actions?: Array<{
        text: string;
        link: string;
        variant?: 'primary' | 'secondary' | 'minimal';
        icon?: string;
        attrs?: Record<string, string | number | boolean>;
    }>;
}

export interface PaginationOption {
    link?: string;
    label?: string;
}

export interface SidebarConfig {
    label?: string;
    order?: number;
    hidden?: boolean;
    badge?: string | BadgeConfig;
    attrs?: Record<string, string | number | boolean | undefined>;
}

export interface FrontmatterConfig {
    author?: string;
    banner?: BannerConfig;
    category?: string;
    description?: string;
    draft?: boolean;
    editUrl?: string | boolean;
    head?: HeadConfig[];
    hero?: HeroConfig;
    lastUpdated?: string;
    next?: boolean | string | PaginationOption;
    pagefind?: boolean;
    prev?: boolean | string | PaginationOption;
    sidebar?: SidebarConfig;
    slug?: string;
    template?: 'doc' | 'splash';
    title: string;
}
````

## File: .gitignore
````
# build output
dist/
# generated types
.astro/

# dependencies
node_modules/

# Test coverage
/coverage/

# logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*


# environment variables
.env
.env.production

# macOS-specific files
.DS_Store
````

## File: .nvmrc
````
v18
````

## File: astro.config.mjs
````
import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwind from '@astrojs/tailwind';

import react from "@astrojs/react";

import {URLS} from './src/Consts';
import {useTranslation} from './src/lib/utils'

// https://astro.build/config
export default defineConfig({
    favicon: './src/assets/hardcover.svg',
    integrations: [starlight({
        components: {
            SocialIcons: './src/components/SocialIcons.astro',
            EditLink: './src/components/PageEdit.astro'
        },
        customCss: ['./src/tailwind.css'],
        defaultLocale: 'root',
        editLink: {
            baseUrl: URLS.GITHUB_EDIT
        },
        head: [
            {
                tag: 'script',
                attrs: {
                    src: 'https://plausible.hardcover.app/js/script.js',
                    'data-domain': 'docs.hardcover.app',
                    defer: true
                },
            },
        ],
        lastUpdated: true,
        locales: {
            // 'es': {
            //     label: useTranslation('lang.label', 'es'),
            //     lang: useTranslation('lang.code', 'es'),
            // },
            // 'fr': {
            //     label: useTranslation('lang.label', 'fr'),
            //     lang: useTranslation('lang.code', 'fr')
            // },
            'it': {
                label: useTranslation('lang.label', 'it'),
                lang: useTranslation('lang.code', 'it')
            },
            // 'pl': {
            //     label: useTranslation('lang.label', 'pl'),
            //     lang: useTranslation('lang.code', 'pl')
            // },
            root: {
                label: useTranslation('lang.label', 'en'),
                lang: useTranslation('lang.code', 'en')
            },
        },
        logo: {
            src: './src/assets/hardcover.svg'
        },
        sidebar: [
            {
                label: useTranslation('sidebar.api.title', 'en'),
                collapsed: true,
                items: [
                    {
                        label: useTranslation('sidebar.api.gettingStarted', 'en'),
                        slug: 'api/getting-started',
                        translations: {
                            es: useTranslation('sidebar.api.gettingStarted', 'es'),
                            fr: useTranslation('sidebar.api.gettingStarted', 'fr'),
                            it: useTranslation('sidebar.api.gettingStarted', 'it'),
                            pl: useTranslation('sidebar.api.gettingStarted', 'pl')
                        }
                    },
                    {
                        label: useTranslation('sidebar.api.guides', 'en'),
                        translations: {
                            es: useTranslation('sidebar.api.guides', 'es'),
                            fr: useTranslation('sidebar.api.guides', 'fr'),
                            it: useTranslation('sidebar.api.guides', 'it'),
                            pl: useTranslation('sidebar.api.guides', 'pl')
                        },
                        autogenerate: {directory: 'api/guides'},
                        collapsed: true,
                    },
                    {
                        label: useTranslation('sidebar.api.schemas', 'en'),
                        translations: {
                            es: useTranslation('sidebar.api.schemas', 'es'),
                            fr: useTranslation('sidebar.api.schemas', 'fr'),
                            it: useTranslation('sidebar.api.schemas', 'it'),
                            pl: useTranslation('sidebar.api.schemas', 'pl')
                        },
                        autogenerate: {directory: 'api/GraphQL/Schemas'},
                        collapsed: true,
                    }
                ]
            },
            {
                label: useTranslation('sidebar.contributing.title', 'en'),
                collapsed: true,
                autogenerate: {directory: 'contributing'},
                translations: {
                    es: useTranslation('sidebar.contributing.title', 'es'),
                    fr: useTranslation('sidebar.contributing.title', 'fr'),
                    it: useTranslation('sidebar.contributing.title', 'it'),
                    pl: useTranslation('sidebar.contributing.title', 'pl')
                }
            },
            {
                label: useTranslation('sidebar.librarians.title', 'en'),
                collapsed: true,
                items: [
                    {
                        label: useTranslation('sidebar.librarians.gettingStarted', 'en'),
                        slug: 'librarians/getting-started',
                    
                        translations: {
                            es: useTranslation('sidebar.librarians.gettingStarted', 'es'),
                            fr: useTranslation('sidebar.librarians.gettingStarted', 'fr'),
                            it: useTranslation('sidebar.librarians.gettingStarted', 'it'),
                            pl: useTranslation('sidebar.librarians.gettingStarted', 'pl')
                        }
                    },
                    // {
                    //     label: useTranslation('sidebar.librarians.editing', 'en'),
                    //     slug: 'librarians/editing',

                    //     translations: {
                    //         es: useTranslation('sidebar.librarians.editing', 'es'),
                    //         fr: useTranslation('sidebar.librarians.editing', 'fr'),
                    //         it: useTranslation('sidebar.librarians.editing', 'it'),
                    //         pl: useTranslation('sidebar.librarians.editing', 'pl')
                    //     }
                    // },
                    {
                        label: useTranslation('sidebar.librarians.faq', 'en'),
                        slug: 'librarians/faq',

                        translations: {
                            es: useTranslation('sidebar.librarians.faq', 'es'),
                            fr: useTranslation('sidebar.librarians.faq', 'fr'),
                            it: useTranslation('sidebar.librarians.faq', 'it'),
                            pl: useTranslation('sidebar.librarians.faq', 'pl')
                        }
                    },
                    {
                        label: useTranslation('sidebar.librarians.resources', 'en'),
                        autogenerate: {directory: 'librarians/Resources'},

                        translations: {
                            es: useTranslation('sidebar.librarians.resources', 'es'),
                            fr: useTranslation('sidebar.librarians.resources', 'fr'),
                            it: useTranslation('sidebar.librarians.resources', 'it'),
                            pl: useTranslation('sidebar.librarians.resources', 'pl')
                        }
                    },
                    {
                        label: useTranslation('sidebar.librarians.standards', 'en'),
                        autogenerate: {directory: 'librarians/Standards'},

                        translations: {
                            es: useTranslation('sidebar.librarians.standards', 'es'),
                            fr: useTranslation('sidebar.librarians.standards', 'fr'),
                            it: useTranslation('sidebar.librarians.standards', 'it'),
                            pl: useTranslation('sidebar.librarians.standards', 'pl')
                        }
                    }
                ],

                translations: {
                    es: useTranslation('sidebar.librarians.title', 'es'),
                    fr: useTranslation('sidebar.librarians.title', 'fr'),
                    it: useTranslation('sidebar.librarians.title', 'it'),
                    pl: useTranslation('sidebar.librarians.title', 'pl')
                }
            }
        ],
        social: {
            discord: URLS.DISCORD,
            github: URLS.GITHUB,
            instagram: URLS.INSTAGRAM,
            mastodon: URLS.MASTODON,
        },
        title: {
            en: useTranslation('site.title', 'en'),
        }
    }), tailwind({
        applyBaseStyles: false
    }), react()],
    site: URLS.DOCS
});
````

## File: components.json
````json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.mjs",
    "css": "src/tailwind.css",
    "baseColor": "slate",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
````

## File: CONTRIBUTING.md
````markdown
# Hardcover Contributing Guidelines

The Hardcover documentation site is an open-source project, and we welcome contributions from the community.
This document outlines the process for contributing to Hardcover.

## Ways to Contribute

We are currently looking for contributions in the following areas:

- API Documentation: Help us improve the API documentation by adding new pages or updating existing content.
- API Guides: Share your knowledge by writing guides on how to use the Hardcover API.
- Bug Fixes: Help us fix bugs in the documentation site.
- Reporting Issues: Report any issues you encounter with the documentation
  site.
  [Create an Issue](https://github.com/hardcoverapp/hardcover-docs/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=)
- Feature Requests: Share your ideas for new features or improvements to the documentation
  site.
  [Suggest a Feature](https://github.com/hardcoverapp/hardcover-docs/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=)
- Librarian Guides: Share your expertise by writing guides on how to use the Librarian tools.

## Finding Something to Work On

You can find issues to work on
by looking at the [Issues Board](https://github.com/hardcoverapp/hardcover-docs/issues) on GitHub
or by joining the [Hardcover Discord](https://discord.gg/edGpYN8ym8) and asking for suggestions in
the [#API](https://discord.com/channels/835558721115389962/1278040045324075050)
or [#librarians](https://discord.com/channels/835558721115389962/1105918193022812282) channels.

## Being a Good Contributor

When contributing to Hardcover, please follow these guidelines:

- Be respectful of others and their contributions.
- Be open to feedback and willing to make changes based on feedback.
- Be patient and understanding of the time it takes to review and merge contributions.
- Be clear and concise in your contributions.
- Be willing to help others and answer questions.
- Be willing to work with others to improve the documentation site.
- Be open to learning and growing as a contributor.
- Be willing to follow the contribution processes.
- Be willing to accept that not all contributions will be accepted.

## Contribution Process

To contribute to Hardcover, follow these steps:

### For Code Contributions

1. Fork the [Hardcover Docs Repository](https://github.com/hardcoverapp/hardcover-docs.git) on GitHub.
2. Clone your fork to your local machine.
3. Create a new branch for your contribution.
4. Follow the [Hardcover Documentation Developer Guide](/DEVELOPERS.md) to set up your local development environment.
5. Make your changes.
6. Test your changes locally.
7. Run `npm run test` to ensure your changes pass the tests.
8. Commit your changes.
9. Push your changes to your fork on GitHub.
10. Create a pull request to the main Hardcover Docs Repository.
11. Notify the Hardcover team, namely `@revelry` in the [Hardcover Discord](https://discord.gg/edGpYN8ym8) that you have
	submitted a pull request.
12. Wait for feedback and review from the Hardcover team.
13. Make any requested changes.
14. Once your pull request is approved, it will be merged into the main branch.
15. Celebrate your contribution!
16. Update your fork with the latest changes from the main branch.
17. Continue contributing to Hardcover!

### For Content Contributions

1. Using the UI navigate to the page you want to edit.
2. Click the "Edit page" button near the bottom of the content.
3. Make your changes in the editor.
4. Preview your changes for formatting and accuracy.
5. Submit your changes opening a pull request.
6. Notify the Hardcover team, namely `@revelry` in the [Hardcover Discord](https://discord.gg/edGpYN8ym8) that you have
   submitted a pull request.
7. Wait for feedback and review from the Hardcover team.
8. Make any requested changes.
9. Once your pull request is approved, it will be merged into the main branch.
10. Celebrate your contribution!
11. Continue contributing to Hardcover!

### For Contribution Suggestions

If you have a suggestion for a contribution, but don't want to make the changes yourself, follow these steps:

1. Create a new issue on the [Issues Board](https://github.com/hardcoverapp/hardcover-docs/issues)
2. Provide a detailed description of the bug or feature request.
3. Wait for feedback and review from the Hardcover team.

## FAQ

### How is the project structured?

#### File Structure

Starlight looks for `.md` or `.mdx` files in the `src/content/docs/` directory.
Each file is exposed as a route based on its file name.

Images can be added to `src/assets/` and embedded in Markdown with a relative link.

Static assets, like favicons, can be placed in the `public/` directory.

### Frontmatter

Each Markdown file can include frontmatter to provide metadata about the document.

| Field           | Description                                                                                                                                                                             | Required    |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| title           | String containing the title of the page                                                                                                                                                 | Yes         |
| category        | String of the category the page should be included in `guide` or `reference`                                                                                                            | Yes         |
| layout          | relative path to `/src/layouts/documentation.astro`                                                                                                                                     | Yes         |
| description     | String containing the descriptive text to use in HTML meta tags                                                                                                                         | Recommended |
| lastUpdated     | String in the format `YYYY-MM-DD HH:MM:SS`                                                                                                                                              | Recommended |
| draft           | Boolean value determining whether the page should be hidden from the production site                                                                                                    | No          |
| slug            | String containing the URL slug for the page                                                                                                                                             | No          |
| tableOfContents | Boolean value determining whether a table of contents should be generated                                                                                                               | No          |
| template        | `doc` or `splash` default is `doc`. `splash` is a wider layout without the normal sidebars                                                                                              | No          |
| hero            | See [Starlight - Frontmatter HeroConfig](https://starlight.astro.build/reference/frontmatter/#heroconfig) for more information                                                          | No          |
| banner          | See [Starlight - Frontmatter Banner](https://starlight.astro.build/reference/frontmatter/#banner) for more information                                                                  | No          |
| prev            | Boolean value determining whether a previous button should be shown. See [Starlight - Frontmatter Prev](https://starlight.astro.build/reference/frontmatter/#prev) for more information | No          |
| next            | Boolean value determining whether a next button should be shown. See [Starlight - Frontmatter Next](https://starlight.astro.build/reference/frontmatter/#next) for more information     | No          |
| sidebar         | Control how the page is displayed in the sidebar. See [Starlight - Frontmatter Sidebar](https://starlight.astro.build/reference/frontmatter/#sidebarconfig) for more information        | No          |

#### Example Frontmatter

```md
---
title: Getting Started with the API
description: Get started with the Hardcover GraphQL API.
category: guide
lastUpdated: 2025-02-01 17:03:00
layout: ../../layouts/documentation.astro
---
```

### Finding Help on Discord

Connect with us on [Discord](https://discord.gg/edGpYN8ym8)
````

## File: DEVELOPERS.md
````markdown
# Hardcover Documentation Developer Guide

## Contributing to the Hardcover Documentation

### [Contributing Guidelines](CONTRIBUTING)

### Developer Code of Conduct

### PR Templates

## Developer FAQs

### How is the project structured?

#### File Structure

Starlight looks for `.md` or `.mdx` files in the `src/content/docs/` directory. 
Each file is exposed as a route based on its file name.

Images can be added to `src/assets/` and embedded in Markdown with a relative link.

Static assets, like favicons, can be placed in the `public/` directory.

### How do I run the project locally?

#### 🚀 Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/hardcoverapp/hardcover-docs.git
    ```
2. **Navigate to the project directory:**
   ```bash
   cd hardcover-docs
   ```
3. **Install dependencies:**
    ```bash
    npm install
    ```
4. **Start the dev server:**
    ```bash
    npm run dev
    ```
5. **Open your browser**
6. **Navigate to `http://localhost:4321`**

#### 🧞 Commands

The Hardcover documentation site is built with [Astro](https://astro.build/).
All commands are run from the root of the project, from a terminal:

| Command                              | Action                                           |
|:-------------------------------------|:-------------------------------------------------|
| `npm install`                        | Installs dependencies                            |
| `npm run dev`                        | Starts local dev server at `localhost:4321`      |
| `npm run build`                      | Build your production site to `./dist/`          |
| `npm run preview`                    | Preview your build locally, before deploying     |
| `npm run astro ...`                  | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help`            | Get help using the Astro CLI                     |
| `npx vitest`                         | Run the unit tests for the project               |
| `npx vitest --coverage.enabled true` | Run the unit tests with code coverage            |

### How do I add a new page or update an existing page?
#### Adding a New Page

1. Create a new `.mdx` file in the `src/content/docs/` directory.
2. Give the file a name that describes the content.
3. Add [frontmatter](#page-frontmatter) to the top of the file.
4. Add content to the file using Markdown or MDX syntax.
5. Add the new page to the sidebar
- If the page is part of the `api/GraphQL/Schema` or `guides` sections the sidebar will automatically update with the new page.
- All other pages will need to be added to the astro config file
  see [Starlight - Add links and link groups](https://starlight.astro.build/guides/sidebar/#add-links-and-link-groups)
  for more information.

##### Page Frontmatter

| Field           | Description                                                                                                                                                                             | Required    |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| title           | String containing the title of the page                                                                                                                                                 | Yes         |
| category        | String of the category the page should be included in `guide` or `reference`                                                                                                            | Yes         |
| layout          | relative path to `/src/layouts/documentation.astro`                                                                                                                                     | Yes         |
| description     | String containing the descriptive text to use in HTML meta tags                                                                                                                         | Recommended |
| lastUpdated     | String in the format `YYYY-MM-DD HH:MM:SS`                                                                                                                                              | Recommended |
| draft           | Boolean value determining whether the page should be hidden from the production site                                                                                                    | No          |
| slug            | String containing the URL slug for the page                                                                                                                                             | No          |
| tableOfContents | Boolean value determining whether a table of contents should be generated                                                                                                               | No          |
| template        | `doc` or `splash` default is `doc`. `splash` is a wider layout without the normal sidebars                                                                                              | No          |
| hero            | See [Starlight - Frontmatter HeroConfig](https://starlight.astro.build/reference/frontmatter/#heroconfig) for more information                                                          | No          |
| banner          | See [Starlight - Frontmatter Banner](https://starlight.astro.build/reference/frontmatter/#banner) for more information                                                                  | No          |
| prev            | Boolean value determining whether a previous button should be shown. See [Starlight - Frontmatter Prev](https://starlight.astro.build/reference/frontmatter/#prev) for more information | No          |
| next            | Boolean value determining whether a next button should be shown. See [Starlight - Frontmatter Next](https://starlight.astro.build/reference/frontmatter/#next) for more information     | No          |
| sidebar         | Control how the page is displayed in the sidebar. See [Starlight - Frontmatter Sidebar](https://starlight.astro.build/reference/frontmatter/#sidebarconfig) for more information        | No          |

###### Example Frontmatter

```md
---
title: Getting Started with the API
description: Get started with the Hardcover GraphQL API.
category: guide
lastUpdated: 2025-02-01 17:03:00
layout: ../../layouts/documentation.astro
---
```

#### Available Components

In addition to the standard [Starlight - Components](https://starlight.astro.build/guides/components/), the Hardcover
documentation site includes the following custom
components:

##### GraphQLExplorer

This component allows a user to view GraphQL queries and experiment by running them against the API.

**Import Path:**

```js
import GraphQLExplorer from '@/components/GraphQLExplorer/GraphQLExplorer.astro';
```

**Parameters:**

- `canTry` - A boolean value determining whether the user can run the query in the explorer. The default is `true`.
- `description` - A string describing the query.
- `forcePresentation` - A boolean value determining whether the presentation options should be hidden. The default is `false`.
- `presentation` - The default presentation of the response, either `json` or `table`. The default is `json`.
- `query` - A string containing the GraphQL query to be displayed in the explorer.
- `title` - A string for the title of the query shown in the explorer. The default is `Example Query`. Change this when translating the page to another language.

**Usage:**

```mdx
<GraphQLExplorer
    query={query}
    description="An example query"
    presentation='table'
    title="Example"
/>
```

### How do I add a new language to the language dropdown?

The root language should **not** be changed from English. To add a new language, see [Starlight - Configure i18n](https://starlight.astro.build/guides/i18n/#configure-i18n).

When adding a new language, you should also update the existing translations in the astro config file to include the new language.

### How do I add a translation for an existing language?

Once a language has been added to the Astro config file you can create a new file in the `src/content/docs/` directory
inside a folder named with the language code. This new file should have the same name as the original file you are translating.

For example, if you are translating the `src/content/docs/getting-started.mdx` file into Spanish you would create a new
file at `src/content/docs/es/getting-started.mdx` with the Spanish translation of the content.

## Support Resources

### Submitting a Bug Report

### Requesting a Feature

### Finding Help on Discord
Connect with us on [Discord](https://discord.gg/edGpYN8ym8)
````

## File: LICENSE.md
````markdown
MIT License

Copyright (c) 2024 Hardcover LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````

## File: package.json
````json
{
  "name": "hardcover-docs",
  "description": "Documentation for the Hardcover APIs",
  "repository": "https://github.com/RevelryPlay/hardcover-doc",
  "author": "RevelryPlay",
  "type": "module",
  "version": "0.0.1",
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro check && astro build",
    "preview": "astro preview",
    "astro": "astro",
    "test": "vitest"
  },
  "dependencies": {
    "@astrojs/check": "^0.9.4",
    "@astrojs/react": "^4.1.2",
    "@astrojs/starlight": "^0.30.3",
    "@astrojs/starlight-tailwind": "^3.0.0",
    "@astrojs/tailwind": "^5.1.4",
    "@radix-ui/react-accordion": "^1.2.8",
    "@radix-ui/react-label": "^2.1.0",
    "@radix-ui/react-popover": "^1.1.11",
    "@radix-ui/react-scroll-area": "^1.1.0",
    "@radix-ui/react-select": "^2.2.2",
    "@radix-ui/react-separator": "^1.1.0",
    "@radix-ui/react-slot": "^1.1.0",
    "@radix-ui/react-tabs": "^1.1.0",
    "astro": "^5.1.1",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.1",
    "dompurify": "^3.2.4",
    "lucide-react": "^0.441.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-icons": "^5.3.0",
    "sharp": "^0.32.5",
    "tailwind-merge": "^2.5.2",
    "tailwindcss": "^3.4.4",
    "tailwindcss-animate": "^1.0.7",
    "typescript": "^5.5.4"
  },
  "devDependencies": {
    "@testing-library/dom": "^10.4.0",
    "@testing-library/jest-dom": "^6.5.0",
    "@testing-library/react": "^16.0.1",
    "@testing-library/user-event": "^14.5.2",
    "@types/react": "^18.3.8",
    "@types/react-dom": "^18.3.0",
    "@vitest/coverage-v8": "^3.1.2",
    "jsdom": "^25.0.1",
    "vitest": "^3.1.2"
  }
}
````

## File: README.md
````markdown
<img src="src/assets/hardcover.svg" alt="Hardcover Logo" width="200">

# Hardcover API Documentation
[Discover Hardcover](https://hardcover.app/) - [View Documentation](https://docs.hardcover.app) - [Connect with us on Discord](https://discord.gg/edGpYN8ym8)

[![Deploy to GitHub Pages](https://github.com/hardcoverapp/hardcover-docs/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/hardcoverapp/hardcover-docs/actions/workflows/deploy.yml)

## Book Smart
Track every book, share them with the world (or don't), and find new life-changing reads.

### Find
Search and browse for new books – or find inspiration in other reader's libraries.

### Track
Track every book by want to read, currently reading, read, and did not finish.

### Connect
Explore other reader's bookshelves and follow for their next reads.

### Discover
Use our amazing stats and tools, including AI, to discover new horizons in your reading journey.

## Contributing to the Hardcover Documentation
- [Contributing Guidelines](CONTRIBUTING.md)
- [Developer Guidelines](DEVELOPERS.md)

### 🚀 Quick Start
1. **Clone the repo:**
   ```bash
   git clone https://github.com/hardcoverapp/hardcover-docs.git
    ```
2. **Navigate to the project directory:**
   ```bash
   cd hardcover-docs
   ```
3. **Install dependencies:**
    ```bash
    npm install
    ```
4. **Start the dev server:**
    ```bash
    npm run dev
    ```
5. **Open your browser**
6. **Navigate to `http://localhost:4321`**
````

## File: tailwind.config.mjs
````
import starlightPlugin from '@astrojs/starlight-tailwind';

// Generated color palettes
const accent = { 200: '#b6c8f4', 600: '#3d5dda', 900: '#1d2d63', 950: '#172143' };
const gray = { 100: '#f6f6f8', 200: '#ededf2', 300: '#c1c1c7', 400: '#898b95', 500: '#565761', 700: '#363741', 800: '#25262f', 900: '#17181c' };


/** @type {import('tailwindcss').Config} */
export default {
    // darkMode: ['class'],
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
    	extend: {
    		colors: {
				accent,
				gray,
			},
    		borderRadius: {
    			lg: 'var(--radius)',
    			md: 'calc(var(--radius) - 2px)',
    			sm: 'calc(var(--radius) - 4px)'
    		}
    	}
    },
	plugins: [starlightPlugin(), require("tailwindcss-animate")],
};
````

## File: tsconfig.json
````json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": [
        "./src/*"
      ]
    },
    "jsx": "react-jsx",
    "jsxImportSource": "react"
  }
}
````

## File: vitest-setup.js
````javascript
import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'

// runs a clean after each test case (e.g. clearing jsdom)
afterEach(() => {
    cleanup();
})
````

## File: vitest.config.ts
````typescript
/// <reference types="vitest" />
import {defineConfig} from 'vitest/config';
import { resolve } from 'path';

export default defineConfig(
    {
        test: {
            coverage: {
                reporter: ['text', 'json-summary', 'json'],
                reportOnFailure: true,
            },
            environment: 'jsdom',
            globals: true,
            setupFiles: './vitest-setup.js',
        },
        resolve: {
            alias: {
                '@': resolve(__dirname, 'src'),
            },
        }
    }
);
````
